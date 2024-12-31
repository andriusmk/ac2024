//
//  day21test.swift
//  day21test
//
//  Created by Andrius Mazeikis on 30/12/2024.
//

import Testing

struct day21test {
    let keypadMap: [Character: Vector2D] = [
        "7": Vector2D(0, 0),
        "8": Vector2D(1, 0),
        "9": Vector2D(2, 0),
        "4": Vector2D(0, 1),
        "5": Vector2D(1, 1),
        "6": Vector2D(2, 1),
        "1": Vector2D(0, 2),
        "2": Vector2D(1, 2),
        "3": Vector2D(2, 2),
        "0": Vector2D(1, 3),
        "A": Vector2D(2, 3)
    ]

    let panelMap: [Command: Vector2D] = [
        .up: Vector2D(1, 0),
        .act: Vector2D(2, 0),
        .left: Vector2D(0, 1),
        .down: Vector2D(1, 1),
        .right: Vector2D(2, 1)
    ]
    
    let translator: Translator<Character>

    init() {
        let keypad = makeTranslator(map: keypadMap, dead: Vector2D(0, 3), start: "A")
        let panel = makeTranslator(map: panelMap, dead: Vector2D(0, 0), start: .act)
        translator = keypad | panel | panel
    }

    @Test(arguments: [
        ("029A", 68),
        ("980A", 60),
        ("179A", 68),
        ("456A", 64),
        ("379A", 64)
    ]) func example(input: String, cnt: Int) throws {
        #expect(translator.translate(input).count(where: {_ in true}) == cnt)
    }
    
    @Test func fullExample() throws {
        let data = """
        029A
        980A
        179A
        456A
        379A
        """
        func toComplexity(_ code: Substring) -> Int {
            translator.translate(code).count(where: {_ in true})
        }
        let codes = data.split(whereSeparator: \.isNewline)
        let products = codes.map{ code in
            guard let value = Int(code.dropLast()) else {return 0}
            let cmpl = toComplexity(code)
            return value * cmpl
        }
        let result = products.reduce(0, (+))
        #expect(result == 126384)
    }
}
