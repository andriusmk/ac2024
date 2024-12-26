//
//  day16test.swift
//  day16test
//
//  Created by Andrius Mazeikis on 19/12/2024.
//

import Testing

struct Tests {
    
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
    
    @Test("Examples from the task", arguments: [("""
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
        """, (7036, 45)),
        ("""
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
        """, (11048, 64))
    ])
    func examples(data: String, expected: (Int, Int)) throws {
        let maze = try #require(parse(data))
        let result = try #require(findCheapestPath(maze: maze))
        #expect(result == expected)
    }
}
