//
//  Day20test.swift
//  Day20test
//
//  Created by Andrius Mazeikis on 03/01/2025.
//

import Testing

struct Day20test {
    let data = """
    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..E#...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############
    """

    @Test func example1() throws {
        let maze: Maze! = parse(data)
        try #require(maze != nil)
        var processor: Processor! = Processor(maze, limits: [2], minimum: 2)
        try #require(processor != nil)
        processor.process(data)
        let stats = processor.stats[0]
        #expect(stats[2] == 14)
        #expect(stats[4] == 14)
        #expect(stats[6] == 2)
        #expect(stats[8] == 4)
        #expect(stats[10] == 2)
        #expect(stats[12] == 3)
        #expect(stats[20] == 1)
        #expect(stats[36] == 1)
        #expect(stats[38] == 1)
        #expect(stats[40] == 1)
        #expect(stats[64] == 1)
    }
    
    @Test func example2() throws {
        let maze: Maze! = parse(data)
        try #require(maze != nil)
        var processor: Processor! = Processor(maze, limits: [2, 20], minimum: 50)
        try #require(processor != nil)
        processor.process(data)
        let stats = processor.stats[1]
        #expect(stats[50] == 32)
        #expect(stats[52] == 31)
        #expect(stats[54] == 29)
        #expect(stats[56] == 39)
        #expect(stats[58] == 25)
        #expect(stats[60] == 23)
        #expect(stats[62] == 20)
        #expect(stats[64] == 19)
        #expect(stats[66] == 12)
        #expect(stats[68] == 14)
        #expect(stats[70] == 12)
        #expect(stats[72] == 22)
        #expect(stats[74] == 4)
        #expect(stats[76] == 3)
    }
}
