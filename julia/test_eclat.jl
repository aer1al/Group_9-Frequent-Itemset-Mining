using Test
using Random

include(joinpath(@__DIR__, "EclatJulia.jl"))
using .EclatJulia

root = normpath(joinpath(@__DIR__, ".."))

@testset "Eclat Julia - Correctness" begin

    toy = read_transactions(
        joinpath(root, "data", "toy", "baskets.txt")
    )

    expected = Dict(
        (1,) => 4,
        (2,) => 5,
        (3,) => 4,
        (1, 2) => 3,
        (1, 3) => 3,
        (2, 3) => 3,
        (1, 2, 3) => 2
    )

    for backend in (:set, :bitset)
        result = mine(toy, 2; backend=backend)

        @test result.supports == expected
        @test result.transactions == 6
        @test result.min_count == 2

        relative = mine(toy, 0.5; backend=backend)
        @test relative.min_count == 3
        @test length(relative.supports) == 6
    end

    repeated = [
        [1, 1, 2],
        [1, 2],
        [2],
        [1]
    ]

    for backend in (:set, :bitset)
        r = mine(repeated, 2; backend=backend)
        @test r.supports == Dict(
            (1,) => 3,
            (2,) => 3,
            (1, 2) => 2
        )
    end

    @test_throws ArgumentError mine(toy, 0)
    @test_throws ArgumentError mine(toy, -1)
    @test_throws ArgumentError mine(toy, 2.5)
    @test_throws ArgumentError mine(toy, 2; backend=:wrong)
    @test_throws ArgumentError mine(Vector{Vector{Int}}(), 1)

end

@testset "Eclat Julia - Random vs Brute Force" begin

    rng = MersenneTwister(2026)

    for trial in 1:30
        transactions = [
            [item for item in 1:5 if rand(rng, Bool)]
            for _ in 1:8
        ]

        minsup = rand(rng, 1:5)
        brute = Dict{Tuple{Vararg{Int}}, Int}()

        for mask in 1:31
            items = [
                item for item in 1:5
                if (mask & (1 << (item - 1))) != 0
            ]

            support = count(
                row -> all(item -> item in row, items),
                transactions
            )

            if support >= minsup
                brute[Tuple(items)] = support
            end
        end

        for backend in (:set, :bitset)
            result = mine(
                transactions, minsup;
                backend=backend
            )
            @test result.supports == brute
        end
    end

end

println("Julia Eclat correctness tests completed.")
