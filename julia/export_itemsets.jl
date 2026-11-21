include(joinpath(@__DIR__, "EclatJulia.jl"))
using .EclatJulia

root = normpath(joinpath(@__DIR__, ".."))
csv = joinpath(root, "results", "julia_benchmark.csv")
output = joinpath(root, "results", "julia_itemsets.csv")

cases = Set{Tuple{String, Int}}()

for line in readlines(csv)[2:end]
    fields = split(strip(line), ",")
    if fields[3] == "bitset" && lowercase(fields[7]) == "true"
        push!(cases, (String(fields[1]), parse(Int, fields[2])))
    end
end

@assert length(cases) == 24

open(output, "w") do io
    println(io, "dataset,min_count,itemset,support")

    for dataset in sort(unique([c[1] for c in cases]))
        path = joinpath(root, "data", "benchmark", dataset * ".txt")
        transactions = read_transactions(path)

        thresholds = sort([c[2] for c in cases if c[1] == dataset])

        for minsup in thresholds
            result = mine(transactions, minsup; backend=:bitset)

            for (items, support) in result.supports
                println(io,
                    dataset, ",",
                    minsup, ",",
                    join(items, " "), ",",
                    support
                )
            end

            println(dataset, " | minsup=", minsup,
                    " | itemsets=", length(result.supports))
        end
    end
end

println("Created: ", output)
