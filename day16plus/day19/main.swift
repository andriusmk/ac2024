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
    let re: Regex<Substring>
    
    init(_ blocks: [String]) throws {
        let joinedBlocks = blocks.joined(separator: "|")
        re = try Regex("(?:\(joinedBlocks))*")
    }
    
    func matching(_ pattern: String) -> Bool {
        return (try? re.wholeMatch(in: pattern)) != nil
    }
}

let (blocks, patterns) = parse(try String(contentsOfFile: "input", encoding: .ascii))
let checker = try PatternChecker(blocks)
let result = patterns.filter(checker.matching).count
print(result)
