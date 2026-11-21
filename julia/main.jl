include(joinpath(@__DIR__, "EclatJulia.jl"))
using .EclatJulia

function main(args)
    if "--help" in args || "-h" in args
        println("Usage:")
        println("julia julia/main.jl --input FILE --minsup VALUE --output FILE [--backend set|bitset]")
        println("minsup: 0.5 means 50%; 2 means absolute support 2")
        return
    end

    if isodd(length(args))
        error("Arguments must be --key value pairs")
    end

    options = Dict{String, String}()

    for i in 1:2:length(args)
        key = args[i]
        value = args[i + 1]

        startswith(key, "--") ||
            error("Invalid argument: $key")

        key in ("--input", "--minsup", "--output", "--backend") ||
            error("Unknown option: $key")

        options[key] = value
    end

    for required in ("--input", "--minsup", "--output")
        haskey(options, required) ||
            error("Missing argument: $required")
    end

    input_path = options["--input"]
    output_path = options["--output"]
    minsup_text = options["--minsup"]
    backend = Symbol(get(options, "--backend", "bitset"))

    isfile(input_path) ||
        error("Input file not found: $input_path")

    minsup = if occursin(r"^[0-9]+$", minsup_text)
        parse(Int, minsup_text)
    else
        parse(Float64, minsup_text)
    end

    transactions = read_transactions(input_path)

    result = mine(
        transactions,
        minsup;
        backend=backend
    )

    patterns = collect(keys(result.supports))

    sort!(patterns; lt=(a, b) ->
        length(a) == length(b) ?
        isless(a, b) :
        length(a) < length(b)
    )

    mkpath(dirname(abspath(output_path)))

    open(output_path, "w") do io
        for items in patterns
            support = result.supports[items]

            println(
                io,
                join(items, " "),
                " #SUP: ",
                support
            )
        end
    end

    println("=== ECLAT JULIA CLI ===")
    println("Input: ", input_path)
    println("Transactions: ", result.transactions)
    println("Backend: ", backend)
    println("Minimum support count: ", result.min_count)
    println("Frequent itemsets: ", length(patterns))
    println("Output: ", output_path)
end

main(ARGS)
