//
//  main.swift
//  day21
//
//  Created by Andrius Mazeikis on 30/12/2024.
//

import Foundation

struct Blueprint<T: Hashable> {
    let map: [T: Vector2D]
    let start: T
}

enum Command: String {
    case up = "^"
    case down = "v"
    case left = "<"
    case right = ">"
    case act = "A"
}

struct Action<T: Hashable>: Hashable {
    let previous: T
    let current: T
    init(_ from: T, _ to: T) {
        previous = from
        current = to
    }
}

func makeActions<T: Hashable>(start: T, _ seq: any Sequence<T>) -> [Action<T>] {
    let result = seq.reduce((start, []), {
        prev, value in
        (value, prev.1 + [Action(prev.0, value)])}).1
    return result
}

struct Translator<T: Hashable> {
    let map: [Action<T>: any Sequence<Command>]
    let start: T
    
    func translate(_ input: any Sequence<T>) -> any Sequence<Command> {
        let actions: any Sequence<Action<T>> = makeActions(start: start, input)
        let result: [any Sequence<Command>] = actions.compactMap({map[$0]})
        return result.map({AnySequence($0)}).joined()
    }
}

func makeTranslator<T: Hashable>(map: [T: Vector2D], dead: Vector2D, start: T) -> Translator<T>{
    var outMap: [Action<T>: any Sequence<Command>] = [:]
    for (k1, p1) in map {
        for (k2, p2) in map {
            let action = Action(k1, k2)
            let move = p2 + (-p1)
            let vCmd = move.y < 0 ? Command.up : Command.down
            let hCmd = move.x < 0 ? Command.left : Command.right
            let vRep = abs(move.y)
            let hRep = abs(move.x)
            let commands = hCmd == .left && p1.y == dead.y && p2.x == dead.x ?
                            [repeatElement(vCmd, count: vRep),
                            repeatElement(hCmd, count: hRep),
                             repeatElement(.act, count: 1)] :
                            [repeatElement(hCmd, count: hRep),
                             repeatElement(vCmd, count: vRep),
                             repeatElement(.act, count: 1)]
            outMap[action] = commands.joined()
        }
    }
    return Translator(map: outMap, start: start)
}

func |<T: Hashable>(leftSide: Translator<T>, rightSide: Translator<Command>) -> Translator<T> {
    let newMap = leftSide.map.reduce(into: [Action<T>: any Sequence<Command>]()) {
        acc, kv in
        let (key, value) = kv
        acc[key] = rightSide.translate(value)
    }
    return Translator(map: newMap, start: leftSide.start)
}

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

let keypad = makeTranslator(map: keypadMap, dead: Vector2D(0, 3), start: "A")
let panel = makeTranslator(map: panelMap, dead: Vector2D(0, 0), start: .act)

let myPanel = keypad | panel | panel

let result = myPanel.translate("379A")
print(result.count(where: {_ in true}))

print(result.map(\.rawValue).joined())
