include(joinpath(@__DIR__, "EclatJulia.jl"))
using .EclatJulia

root = normpath(joinpath(@__DIR__, ".."))

function load_python_counts(path)
    lines = readlines(path)
    isempty(lines) && error("Empty benchmark CSV")

    header = split(strip(first(lines)), ",")
    columns = Dict(
        String(name) => i
        for (i, name) in enumerate(header)
    )

    required = [
        "dataset", "min_count", "backend",
        "itemset_count", "status"
    ]

    for name in required
        haskey(columns, name) ||
            error("Missing CSV column: $name")
    end

    expected = Dict{Tuple{String, Int}, Int}()

    for line in lines[2:end]
        cells = split(strip(line), ",")

        if length(cells) < maximum(values(columns))
            continue
        end

        if cells[columns["status"]] != "ok" ||
           cells[columns["backend"]] != "bitset"
            continue
        end

        dataset = String(cells[columns["dataset"]])
        minsup = parse(Int, cells[columns["min_count"]])
        pattern_count = parse(
            Int, cells[columns["itemset_count"]]
        )

        expected[(dataset, minsup)] = pattern_count
    end

    return expected
end

function main()
    expected = load_python_counts(
        joinpath(root, "results", "benchmark.csv")
    )

    println("Python reference cases: ", length(expected))

    length(expected) == 24 ||
        error("Expected 24 dataset/minsup pairs")

    # Warm up Julia before measuring runtime.
    toy = read_transactions(
        joinpath(root, "data", "toy", "baskets.txt")
    )

    mine(toy, 2; backend=:set)
    mine(toy, 2; backend=:bitset)

    output = joinpath(
        root, "results", "julia_benchmark.csv"
    )

    passed = 0
    failed = 0

    open(output, "w") do io
        println(
            io,
            "dataset,min_count,backend,seconds," *
            "itemset_count,expected_python_count," *
            "count_match,backend_exact_match"
        )

        datasets = sort(unique([
            key[1] for key in keys(expected)
        ]))

        for dataset in datasets
            file = joinpath(
                root, "data", "benchmark",
                dataset * ".txt"
            )

            isfile(file) ||
                error("Missing dataset: $file")

            transactions = read_transactions(file)

            thresholds = sort(
                [
                    key[2] for key in keys(expected)
                    if key[1] == dataset
                ];
                rev=true
            )

            println(
                "\nDataset: ", dataset,
                " | transactions: ", length(transactions)
            )

            for minsup in thresholds
                baseline = nothing

                for backend in (:set, :bitset)
                    GC.gc()

                    start = time_ns()

                    result = mine(
                        transactions, minsup;
                        backend=backend
                    )

                    seconds = (time_ns() - start) / 1e9

                    count_ok = (
                        length(result.supports) ==
                        expected[(dataset, minsup)]
                    )

                    exact_ok = if backend == :set
                        baseline = result.supports
                        true
                    else
                        result.supports == baseline
                    end

                    ok = count_ok && exact_ok

                    if ok
                        passed += 1
                    else
                        failed += 1
                    end

                    println(
                        io,
                        join(
                            [
                                dataset,
                                minsup,
                                backend,
                                round(seconds; digits=6),
                                length(result.supports),
                                expected[(dataset, minsup)],
                                count_ok,
                                exact_ok
                            ],
                            ","
                        )
                    )

                    println(
                        dataset,
                        " | minsup=", minsup,
                        " | ", backend,
                        " | patterns=", length(result.supports),
                        " | seconds=", round(seconds; digits=6),
                        " | PASS=", ok
                    )
                end
            end
        end
    end

    println("\nSaved: ", output)
    println("Passed: ", passed, "/48")
    println("Failed: ", failed)

    failed == 0 || error("Julia benchmark checks failed")
end

main()
