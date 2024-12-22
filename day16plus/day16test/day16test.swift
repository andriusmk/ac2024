//
//  day16test.swift
//  day16test
//
//  Created by Andrius Mazeikis on 19/12/2024.
//

import Testing

@Suite struct MazeTest {
    let maze = """
    ####
    #S.#
    #.E#
    ####
    """
    
    @Test func validMapNotNil() throws {
        #expect((parse(maze) != nil))
    }
    
    @Test func validContainsWalkables() throws {
        #expect((parse(maze)?.obstacles.isEmpty == false))
    }
}

@Test func example1() throws {
    let maze = parse("""
    ###############
    #.......#....E#
    #.#.###.#.###.#
    #.....#.#...#.#
    #.###.#####.#.#
    #.#.#.......#.#
    #.#.#####.###.#
    #...........#.#
    ###.#.#####.#.#
    #...#.....#.#.#
    #.#.#.###.#.#.#
    #.....#...#.#.#
    #.###.#.#.#.#.#
    #S..#.....#...#
    ###############
    """)
    let result = findCheapestPath(maze: maze!)
    #expect(result != nil)
    #expect(result!.0 == 7036)
    #expect(result!.1 == 45)
}

@Test func example2() throws {
    let maze = parse("""
    #################
    #...#...#...#..E#
    #.#.#.#.#.#.#.#.#
    #.#.#.#...#...#.#
    #.#.#.#.###.#.#.#
    #...#.#.#.....#.#
    #.#.#.#.#.#####.#
    #.#...#.#.#.....#
    #.#.#####.#.###.#
    #.#.#.......#...#
    #.#.###.#####.###
    #.#.#...#.....#.#
    #.#.#.#####.###.#
    #.#.#.........#.#
    #.#.#.#########.#
    #S#.............#
    #################
    """)
    let result = findCheapestPath(maze: maze!)
    #expect(result != nil)
    #expect(result!.0 == 11048)
    #expect(result!.1 == 64)
}
