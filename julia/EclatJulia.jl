module EclatJulia

export MiningResult, min_support_count, read_transactions, mine

struct MiningResult
    supports::Dict{Tuple{Vararg{Int}}, Int}
    transactions::Int
    min_count::Int
end

function min_support_count(minsup::Real, n::Int)
    n > 0 || throw(ArgumentError("Empty database"))
    minsup isa Bool && throw(ArgumentError("Invalid minsup"))

    x = Float64(minsup)
    (isfinite(x) && x > 0) ||
        throw(ArgumentError("minsup must be positive and finite"))

    if minsup isa Integer || x > 1
        isinteger(x) ||
            throw(ArgumentError("Absolute minsup must be integer"))
        return Int(x)
    end

    return max(1, ceil(Int, x * n - 1e-12))
end

function read_transactions(path::AbstractString)
    rows = Vector{Vector{Int}}()

    for (line_no, raw) in enumerate(eachline(path))
        line = strip(replace(raw, '\ufeff' => ""))

        if startswith(line, "#") ||
           startswith(line, "%") ||
           startswith(line, "@")
            continue
        end

        if isempty(line)
            push!(rows, Int[])
            continue
        end

        values = try
            parse.(Int, split(line))
        catch
            throw(ArgumentError("Invalid item at line $line_no"))
        end

        if any(x -> x == -1 || x == -2, values)
            throw(ArgumentError("Sequential format is unsupported"))
        end

        push!(rows, unique(values))
    end

    isempty(rows) && throw(ArgumentError("No transactions"))
    return rows
end

function mine(transactions::AbstractVector, minsup::Real = 0.3;
              backend::Symbol = :bitset,
              max_results::Int = 1_000_000)

    backend in (:set, :bitset) ||
        throw(ArgumentError("Backend must be :set or :bitset"))

    n = length(transactions)
    threshold = min_support_count(minsup, n)

    vertical = Dict{Int, Set{Int}}()

    for (tid, transaction) in enumerate(transactions)
        for item in unique(Int.(collect(transaction)))
            tids = get!(vertical, item) do
                Set{Int}()
            end
            push!(tids, tid)
        end
    end

    singles = [
        (item, tids)
        for (item, tids) in vertical
        if length(tids) >= threshold
    ]

    sort!(singles; by = x -> (length(x[2]), x[1]))

    supports = Dict{Tuple{Vararg{Int}}, Int}()

    function save_result!(chosen::Vector{Int}, support::Int)
        key = Tuple(sort(chosen))
        supports[key] = support

        if length(supports) > max_results
            error("Result cap exceeded; output is incomplete")
        end
    end

    if backend == :set
        extensions = [
            (item, tids) for (item, tids) in singles
        ]

        function dfs_set!(prefix, nodes)
            for i in eachindex(nodes)
                item, tids = nodes[i]
                chosen = vcat(prefix, item)

                save_result!(chosen, length(tids))

                children = Tuple{Int, Set{Int}}[]

                for j in (i + 1):length(nodes)
                    other_item, other_tids = nodes[j]
                    overlap = intersect(tids, other_tids)

                    if length(overlap) >= threshold
                        push!(children, (other_item, overlap))
                    end
                end

                isempty(children) || dfs_set!(chosen, children)
            end
        end

        dfs_set!(Int[], extensions)

    else
        extensions = Tuple{Int, BitVector}[]

        for (item, tids) in singles
            bits = falses(n)

            for tid in tids
                bits[tid] = true
            end

            push!(extensions, (item, bits))
        end

        function dfs_bitset!(prefix, nodes)
            for i in eachindex(nodes)
                item, bits = nodes[i]
                chosen = vcat(prefix, item)

                save_result!(chosen, count(identity, bits))

                children = Tuple{Int, BitVector}[]

                for j in (i + 1):length(nodes)
                    other_item, other_bits = nodes[j]
                    overlap = bits .& other_bits
                    support = count(identity, overlap)

                    if support >= threshold
                        push!(children, (other_item, overlap))
                    end
                end

                isempty(children) || dfs_bitset!(chosen, children)
            end
        end

        dfs_bitset!(Int[], extensions)
    end

    return MiningResult(supports, n, threshold)
end

end
