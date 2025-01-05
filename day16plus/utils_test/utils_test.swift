//
//  utils_test.swift
//  utils_test
//
//  Created by Andrius Mazeikis on 05/01/2025.
//

import Testing

struct utils_test {

    @Test func modInverseTest() throws {
        #expect(modInverse(a: 3, mod: 11) == 4)
        #expect(modInverse(a: 35, mod: 3) == 2)
        #expect(modInverse(a: 21, mod: 5) == 1)
        #expect(modInverse(a: 15, mod: 7) == 1)
    }
}
