//
//  main.swift
//  day23
//
//  Created by Andrius Mazeikis on 06/01/2025.
//

import Foundation

func findEdges(from conns: some Sequence<[String]>)
-> [String: Set<String>] {
    var edges = [String: Set<String>]()
    for conn in conns {
        let s1 = conn[0]
        let s2 = conn[1]
        edges[s1, default: Set()].insert(s2)
        edges[s2, default: Set()].insert(s1)
    }
    return edges
    
}

func identifyTriplets(_ edges: [String: Set<String>]) -> [[String]] {
    var triplets = Set<[String]>()
    for (key, values) in edges {
        for value in values {
            for third in values.intersection(edges[value]!) {
                triplets.insert([key, value, third].sorted())
            }
        }
    }
    return triplets.sorted(by: {$0.joined() < $1.joined()})
}

func parse(_ data: String) -> some Sequence<[String]> {
    data.split(whereSeparator: \.isNewline)
        .map{ $0.split(separator: "-").map{String($0)}}
}

struct Cliques {
    let edges: [String: Set<String>]
    var cliques = [Set<String>]()
    
    mutating func bronKerbosch(rs: Set<String>, ps: Set<String>, xs: Set<String>) {
        var ps = ps
        var xs = xs
        
        if ps.isEmpty && xs.isEmpty {
            cliques.append(rs)
            return
        }
        
        while let vertex = ps.first {
            let newR = rs.union([vertex])
            let adjacent = edges[vertex]!
            let newP = ps.intersection(adjacent)
            let newX = xs.intersection(adjacent)
            bronKerbosch(rs: newR, ps: newP, xs: newX)
            ps.remove(vertex)
            xs.insert(vertex)
        }
    }
}

func findCliques(edges: [String: Set<String>]) -> [Set<String>] {
    var cliques = Cliques(edges: edges)
    cliques.bronKerbosch(rs: Set(), ps: Set(edges.keys), xs: Set())
    return cliques.cliques
}

let data = parse(try String(contentsOfFile: "input", encoding: .ascii))

let result1 = identifyTriplets(findEdges(from: data))
    .filter({$0.contains(where: {$0.starts(with: "t")})}).count

let result2 = findCliques(edges: findEdges(from: data))
    .max(by: {$0.count < $1.count})!
    .sorted()
    .joined(separator: ",")

print(result1, result2)
