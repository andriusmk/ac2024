//
//  day19test.swift
//  day19test
//
//  Created by Andrius Mazeikis on 29/12/2024.
//

import Testing

struct day19test {
    let exampleData = """
    r, wr, b, g, bwu, rb, gb, br

    brwrr
    bggr
    gbbr
    rrbgbr
    ubwu
    bwurrg
    brgr
    bbrgwb
    """
    let blocks = ["r", "wr", "b", "g", "bwu", "rb", "gb", "br"]

    @Test func example() throws {
        let (blocks, patterns) = parse(exampleData)
        #expect(blocks == ["r", "wr", "b", "g", "bwu", "rb", "gb", "br"])
        #expect(patterns == [   "brwrr",
                                "bggr",
                                "gbbr",
                                "rrbgbr",
                                "ubwu",
                                "bwurrg",
                                "brgr",
                                "bbrgwb"
                            ])
    }

    @Test(arguments: ["brwrr",
                      "bggr",
                      "gbbr",
                      "rrbgbr",
                      "bwurrg",
                      "brgr"])
    func matchPositive(_ pattern: String) throws {
        var checker = try PatternChecker(blocks)
        #expect(checker.matching(pattern) != 0)
    }
    @Test(arguments: ["ubwu",
                      "bbrgwb"])
    func matchNegative(_ pattern: String) throws {
        var checker = try PatternChecker(blocks)
        #expect(checker.matching(pattern) == 0)
    }
}
