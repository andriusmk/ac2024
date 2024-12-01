//
//  day18test.swift
//  day18test
//
//  Created by Andrius Mazeikis on 28/12/2024.
//

import Testing

struct day18test {
    let exampleData = """
    5,4
    4,2
    4,5
    3,0
    2,1
    6,3
    2,4
    1,5
    0,6
    3,3
    2,6
    5,1
    1,2
    5,5
    2,5
    6,5
    1,4
    0,4
    6,4
    1,1
    6,1
    1,0
    0,5
    1,6
    2,0
    """
        

    @Test func example() throws {
        let obstacles = parse(exampleData)
        let maze = FrameMaze(size: Vector2D(7, 7), obstacles: Set(obstacles.prefix(12)))
        var crawler = Crawler(maze)
        let result = crawler.minDistance()
        #expect(result != nil && result! == 22)
    }

}
