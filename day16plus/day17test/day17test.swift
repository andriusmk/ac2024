//
//  day17test.swift
//  day17test
//
//  Created by Andrius Mazeikis on 28/12/2024.
//

import Testing

struct day17test {
    let exampleInput = """
    Register A: 729
    Register B: 0
    Register C: 0
    
    Program: 0,1,5,4,3,0
    """

    @Test func exampleParse() throws {
        let cpu = try parse(exampleInput)
        #expect(cpu.state.regA == 729)
        #expect(cpu.state.regB == 0)
        #expect(cpu.state.regC == 0)
        #expect(cpu.program == [0, 1, 5, 4, 3, 0])
    }
    @Test func exampleRun() throws {
        var cpu = try parse(exampleInput)
        try cpu.run()
        #expect(cpu.progOutput == [4,6,3,5,6,3,5,2,1,0])
    }
}
