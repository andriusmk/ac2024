//
//  main.swift
//  day17
//
//  Created by Andrius Mazeikis on 28/12/2024.
//

import Foundation

enum CpuError: Error {
    case invalidOperand
    case loopDetected
}

struct ToyCpu {
    struct State: Hashable {
        var regA: Int
        var regB: Int
        var regC: Int
        var iptr: Int = 0
        init(_ a: Int, _ b: Int, _ c: Int) {
            regA = a
            regB = b
            regC = c
        }
    }
    var state: State
    var program: [Int]
    var progOutput: [Int] = []
    var seenStates = Set<State>()
    
    init(_ a: Int, _ b: Int, _ c: Int, _ prog: [Int]) {
        state = State(a, b, c)
        program = prog
    }
    
    func combo(_ operand: Int) throws -> Int {
        switch operand {
        case 4:
            state.regA
        case 5:
            state.regB
        case 6:
            state.regC
        case 7:
            throw CpuError.invalidOperand
        default:
            operand
        }
    }
    
    mutating func readInstruction() throws -> (Int, Int)? {
        if seenStates.contains(state) {
            throw CpuError.loopDetected
        }
        seenStates.insert(state)
        if state.iptr < program.count - 1 {
            let result = (program[state.iptr], program[state.iptr + 1])
            state.iptr += 2
            return result
        }
        return nil
    }
    
    func xdv(_ operand: Int, _ dst: inout Int) throws {
        let value = try combo(operand)
        dst = state.regA >> value
    }
    
    mutating func execute(_ opcode: Int, _ operand: Int) throws {
        switch opcode {
        case 0:
            try xdv(operand, &state.regA)
        case 1:
            state.regB = state.regB ^ operand
        case 2:
            state.regB = try combo(operand) & 7
        case 3:
            if state.regA != 0 {
                state.iptr = operand
            }
        case 4:
            state.regB = state.regB ^ state.regC
        case 5:
            progOutput.append(try combo(operand) & 7)
        case 6:
            try xdv(operand, &state.regB)
        case 7:
            try xdv(operand, &state.regC)
        default:
            ()
        }
    }
    
    mutating func run() throws {
        while let (opcode, operand) = try readInstruction() {
            try execute(opcode, operand)
        }
    }
    
    mutating func runCheck() throws -> Bool {
        while let (opcode, operand) = try readInstruction() {
            try execute(opcode, operand)
            if progOutput.count > program.count {
                return false
            }
            let index = progOutput.count - 1
            if index >= 0 {
                if progOutput[index] != program[index] {
                    return false
                }
            }
        }
        print(progOutput)
        return progOutput.count == program.count
    }

    mutating func reset() {
        progOutput.removeAll(keepingCapacity: true)
        state = State(0, 0, 0)
        seenStates.removeAll(keepingCapacity: true)
    }
}

func parse(_ data: String) throws -> ToyCpu {
    let number = try Regex("\\d+")
    let regsProgram = data.split(separator: try Regex("\n\n"))
    let rawRegs = regsProgram[0].split(whereSeparator: \.isNewline)
    let regs = try rawRegs.compactMap({try number.firstMatch(in: $0)?.0}).compactMap({Int($0)})
    let program = regsProgram[1].split(separator: try Regex("\\s+"))[1].split(separator: ",")
        .compactMap{Int($0)}
    
    return ToyCpu(regs[0], regs[1], regs[2], program)
}

var cpu = try parse(String(contentsOfFile: "input", encoding: .ascii))
try cpu.run()
print(cpu.progOutput.map({String($0)}).joined(separator: ","))

//var regA = -1
//print(cpu.program)
//while true {
//    regA += 1
//    cpu.reset()
//    cpu.state.regA = regA
//    do {
//        if try cpu.runCheck() {
//            print(regA)
//            print(cpu.progOutput)
//            break
//        }
//    } catch CpuError.invalidOperand {
//        continue
//    }
//}
