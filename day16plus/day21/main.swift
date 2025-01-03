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

enum InvalidData: Error {
    case missingMapEntry
}

enum Command: String {
    case up = "^"
    case down = "v"
    case left = "<"
    case right = ">"
    case act = "A"
}

func makeCommands(from move: Vector2D) -> (Repeated<Command>, Repeated<Command>) {
    let hCmd = move.x < 0 ? Command.left : .right
    let vCmd = move.y < 0 ? Command.up : .down
    let hDist = abs(move.x)
    let vDist = abs(move.y)
    return (
        repeatElement(hCmd, count: hDist),
        repeatElement(vCmd, count: vDist))
}

struct Strategy {
    var predefined: [Vector2D: [Repeated<Command>]] = [:]
    let activate = repeatElement(Command.act, count: 1)
    
    func horizontalFirst(_ commands: (Repeated<Command>, Repeated<Command>)) -> Output {
        let (hCmds, vCmds) = commands
        return [ hCmds, vCmds, activate ]
    }
    
    func verticalFirst(_ commands: (Repeated<Command>, Repeated<Command>)) -> Output {
        let (hCmds, vCmds) = commands
        return [ vCmds, hCmds, activate ]
    }

    func translate(move: Vector2D) -> Output {
        if let commands = predefined[move] {
            return commands
        }
        let commands = makeCommands(from: move)
        if move.x > 0 {
            return verticalFirst(commands)
        }
        return horizontalFirst(commands)
    }
    typealias Output = [Repeated<Command>]
}

protocol TranslatorProtocol {
    associatedtype InputElement: Hashable
    associatedtype Output: Sequence<Command>
    var strategy: Strategy {get set}
    
    func translate<S: Sequence<InputElement>>(input: S) throws -> Output
}


struct Translator<T: Hashable>: TranslatorProtocol {
    let map: [T: Vector2D]
    let start: T
    let forbidden: Vector2D
    let activate = repeatElement(Command.act, count: 1)
    var strategy = Strategy()
    
    func translate<S: Sequence<T>>(input: S) throws -> Output {
        guard let firstPos = map[start] else {throw InvalidData.missingMapEntry}
        let positions = try input.map { element in
            guard let pos = map[element] else {throw InvalidData.missingMapEntry}
            return pos
        }
        let moves: [Repeated<Command>] = positions.reduce((firstPos, []), {
            acc, pos in
            let (previous, lst) = acc
            let move = pos + (-previous)
            if previous.x == forbidden.x && pos.y == forbidden.y {
                let (hCmds, vCmds) = makeCommands(from: move)
                return (pos, lst + [hCmds, vCmds, activate])
            } else if previous.y == forbidden.y && pos.x == forbidden.x {
                let (hCmds, vCmds) = makeCommands(from: move)
                return (pos, lst + [vCmds, hCmds, activate])
            } else {
                return (pos, lst + strategy.translate(move: move))
            }
        }).1
        
        return moves.joined()
    }
    
    func translateMove(_ pair: Pair<T, T>) throws -> Output {
        guard let p1 = map[pair.first],
              let p2 = map[pair.second]
        else { throw InvalidData.missingMapEntry }
        
        var result = Strategy.Output()
        let move = p2 + (-p1)
        
        if p1.x == forbidden.x && p2.y == forbidden.y {
            let commands = makeCommands(from: move)
            result += strategy.horizontalFirst(commands)
        } else if p1.y == forbidden.y && p2.x == forbidden.x {
            let commands = makeCommands(from: move)
            result += strategy.verticalFirst(commands)
        } else {
            result += strategy.translate(move: move)
        }

        return result.joined()
    }
    
    typealias InputElement = T
    typealias Output = FlattenSequence<Strategy.Output>
}

struct TranslatorPipe<T1: TranslatorProtocol, T2: TranslatorProtocol>: TranslatorProtocol
where T2.InputElement == Command {
    var leftSide: T1
    var rightSide: T2
    var strategy: Strategy {
        get { leftSide.strategy }
        set {
            leftSide.strategy = newValue
            rightSide.strategy = newValue
        }
    }
    
    func translate<S: Sequence<T1.InputElement>>(input: S) throws -> T2.Output {
        let leftResult = try leftSide.translate(input: input)
        return try rightSide.translate(input: leftResult)
    }
    
    typealias InputElement = T1.InputElement
    typealias Output = T2.Output
}

func |<T1: TranslatorProtocol, T2: TranslatorProtocol>(leftSide: T1, rightSide: T2) ->
    TranslatorPipe<T1, T2>
where T2.InputElement == Command {
    return TranslatorPipe(leftSide: leftSide, rightSide: rightSide)
}

struct System {
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
    
    let keypad: Translator<Character>
    let robot: Translator<Command>
    var system: TranslatorPipe<TranslatorPipe<Translator<Character>, Translator<Command>>, Translator<Command>>
    
    func translate2(input: Substring, count: Int) throws -> Int {
        let robotCommands = try keypad.translate(input: input)
        var cache = [Pair<Command, Command>: Int]()
        for pair in pairwise([robot.start] + robotCommands) {
            cache[pair, default: 0] += 1
        }
        for (pair, count) in cache {
            print(pair.first, pair.second, count)
        }
        for _ in 0..<count {
            print(cache.values.reduce(0, (+)))
            let pairCnts = Array(cache)
            cache.removeAll(keepingCapacity: true)
            for (pair, cnt) in pairCnts {
                let commands = try robot.translateMove(pair)
                for cmdPair in pairwise([robot.start] + commands) {
                    cache[cmdPair, default: 0] += cnt
                }
            }
        }
        let result = cache.values.reduce(0, (+))
        print(result)
        return result
    }
    
    init() {
        keypad = Translator(map: keypadMap, start: "A", forbidden: Vector2D(0, 3))
        robot = Translator(map: panelMap, start: .act, forbidden: Vector2D(0, 0))
        system = keypad | robot | robot
    }
}

let system = System()
let codes = try String(contentsOfFile: "input", encoding: .ascii).split(whereSeparator: \.isNewline)
let result = try codes.map({
    try system.system.translate(input: $0).count * Int($0.dropLast())!
}).reduce(0, (+))

let result2 = try codes.map({
    try system.translate2(input: $0, count: 25) * Int($0.dropLast())!
}).reduce(0, (+))

print(result, result2)
