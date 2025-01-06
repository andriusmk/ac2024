//
//  main.swift
//  day22
//
//  Created by Andrius Mazeikis on 06/01/2025.
//

import Foundation

func performStep(_ value: Int, shift: Int) -> Int {
    return ((value << shift) ^ value) % 16777216
}

func makeSecret(_ value: Int) -> Int {
    let s1 = performStep(value, shift: 6)
    let s2 = performStep(s1, shift: -5)
    return performStep(s2, shift: 11)
}

func repeatF<T>(_ initial: T, _ f: @escaping (T) -> T, times: Int) -> T {
    return repeatElement(f, count: times).reduce(initial, {$1($0)})
}

struct Calculator {
    var seqRevenues = [[Int8]: Int]()
    
    func maxRevenue() -> Int? {
        seqRevenues.values.max()
    }
    
    mutating func calculate(from values: [Int]) {
        for value in values {
            calculateRevenues(value)
        }
    }
    
    mutating func calculateRevenues(_ starting: Int) {
        var secret = starting
        var prevPrice = 0
        var priceDiffs = [Int8]()
        var seqs = Set<[Int8]>()
        for i in 0..<2000 {
            secret = makeSecret(secret)
            let price = secret % 10
            if i > 0 {
                let diff = Int8(price - prevPrice)
                priceDiffs.append(diff)
                if priceDiffs.count >= 4 {
                    let seq = Array(priceDiffs.suffix(4))
                    if !seqs.contains(seq) {
                        seqRevenues[seq, default: 0] += price
                        seqs.insert(seq)
                    }
                }
            }
            prevPrice = price
        }
    }
}

let values = try String(contentsOfFile: "input", encoding: .ascii)
    .split(whereSeparator: \.isNewline).compactMap({Int($0)})

let result = values.map({repeatF($0, makeSecret, times: 2000)}).reduce(0, (+))

var calculator = Calculator()
calculator.calculate(from: values)
let result2 = calculator.maxRevenue()!

print(result, result2)
