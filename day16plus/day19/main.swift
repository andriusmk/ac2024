//
//  main.swift
//  day19
//
//  Created by Andrius Mazeikis on 29/12/2024.
//

import Foundation

func parse(_ data: String) -> ([String], [String]) {
    let lines = data.split(whereSeparator: \.isNewline)
    let blocks: [String] = Array(lines[0].split(separator: try! Regex(",\\s*")).map({String($0)}))
    let patterns: [String] = Array(lines[1...].map({String($0)}))
    
    return (blocks, patterns)
}

struct PatternChecker {
    let blocks: [(Regex<Substring>, Int, String)]
    var cache: [String: Int] = [:]
    
    init(_ blocks: [String]) throws {
        self.blocks = try blocks.map({(try Regex<Substring>($0), $0.count, $0)})
    }
    
    mutating func matching(_ pattern: Substring) -> Int {
        if pattern.count == 0 {
            return 1
        }
        let pstring = String(pattern)
        if let cached = cache[pstring] {
            return cached
        }
        let matchingBlocks = blocks.filter({pattern.starts(with: $0.0)})
        let result = matchingBlocks.map({matching(pattern.dropFirst($0.1))})
            .reduce(0, (+))
        cache[pstring] = result
        return result
    }
    
    mutating func matching(_ pattern: String) -> Int {
        return matching(Substring(pattern))
    }
}

let (blocks, patterns) = parse(try String(contentsOfFile: "input", encoding: .ascii))
var checker = try PatternChecker(blocks)
let results = patterns.map({checker.matching($0)})
let possible = results.filter({$0 != 0}).count
let total = results.reduce(0, (+))
print(possible, total)
