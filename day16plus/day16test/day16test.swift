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

@Suite("test findNeighbour")
struct FindNeighbourTest {
    let maze = parse("""
    ########
    ###.####
    ###.#.E#
    ###...##
    #..S####
    #.#.####
    #...####
    ########
    """)
    @Test func testLoop() throws {
        guard let (newState, cost) = findNeighbour(maze: maze!, node: State(pos: Vector2D(3, 5), dir: Vector2D(0, 1))) else {return}
        #expect(newState.pos == Vector2D(3, 4))
        #expect(cost == 3007)
    }
    @Test func testDeadEnd() throws {
        #expect(findNeighbour(maze: maze!, node: State(pos: Vector2D(3, 2), dir: Vector2D(0, -1))) == nil)
    }
    @Test func testFinish() throws {
        guard let (newState, cost) = findNeighbour(maze: maze!, node: State(pos: Vector2D(4, 3), dir: Vector2D(1, 0))) else {return}
        #expect(newState.pos == Vector2D(6, 2))
        #expect(cost == 2003)
    }
    @Test func testIntegration() throws {
        #expect(findCheapestPath(maze: maze!) == 4005)
    }
}

@Test func fullIntegration() throws {
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
    #expect(findCheapestPath(maze: maze!) == 7036)
}
