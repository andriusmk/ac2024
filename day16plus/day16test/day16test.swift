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
        #expect((parse(maze)?.walkable.isEmpty == false))
    }
}
