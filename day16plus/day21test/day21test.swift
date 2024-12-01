//
//  day21test.swift
//  day21test
//
//  Created by Andrius Mazeikis on 30/12/2024.
//

import Testing

struct day21test {
    let system = System()

    @Test(arguments: [
        ("029A", 68),
        ("980A", 60),
        ("179A", 68),
        ("456A", 64),
        ("379A", 64)
    ]) func example(input: String, cnt: Int) throws {
        let result = try system.system.translate(input: input).count(where: {_ in true})
        #expect(result == cnt)
    }
    
    @Test func fullExample() throws {
        let data = """
        029A
        980A
        179A
        456A
        379A
        """
        func toComplexity(_ code: Substring) throws -> Int {
            try system.system.translate(input: code).count(where: {_ in true})
        }
        let codes = data.split(whereSeparator: \.isNewline)
        let products = try codes.map{ code in
            guard let value = Int(code.dropLast()) else {return 0}
            let cmpl = try toComplexity(code)
            return value * cmpl
        }
        let result = products.reduce(0, (+))
        #expect(result == 126384)
    }
}
