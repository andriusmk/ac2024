//
//  dijkstra.swift
//  day16plus
//
//  Created by Andrius Mazeikis on 22/12/2024.
//

protocol GraphEdge {
    associatedtype Vertex : Hashable
    
    var distance: Int { get }
    var target: Vertex { get }
}

protocol GraphTrace {
    associatedtype Edge : GraphEdge
    func append(_ edge: Edge) -> Self
    func merge(with: Self) -> Self
    init()
}

struct NullTrace<E : GraphEdge> : GraphTrace {
    func append(_ edge: E) -> NullTrace {
        return self
    }
    func merge(with: NullTrace) -> NullTrace {
        return self
    }
}

func dijkstra<T : GraphTrace>(with getAdjacent: (T.Edge.Vertex) -> [T.Edge],
                         start: T.Edge.Vertex,
                         isEnd: (T.Edge.Vertex) -> Bool,
                         trace: T = T()) -> (Int, T)? {
    var heads = [start: (0, trace)] // Dictionary<T.Edge.Vertex, (Int, T)>()
    var visited = Set<T.Edge.Vertex>()
    
    if isEnd(start) {
        return (0, trace)
    }
    
    func updateAdjacent(_ edge: T.Edge, _ distance: Int, _ trace: T) {
        let targetDistance = distance + edge.distance
        let newTrace = trace.append(edge)
        if let (storedDistance, storedTrace) = heads[edge.target] {
            if storedDistance > targetDistance {
                heads[edge.target] = (targetDistance, newTrace)
            } else if storedDistance == targetDistance {
                heads[edge.target] = (targetDistance, storedTrace.merge(with: newTrace))
            }
        } else {
            heads[edge.target] = (targetDistance, newTrace)
        }
    }
    
    func nextResult() -> (Int, T)? {
        while let (vertex, (minDistance, headTrace)) = heads.min(by: { $0.1.0 < $1.1.0 }) {
            for edge in getAdjacent(vertex).filter({!visited.contains($0.target)}) {
                updateAdjacent(edge, minDistance, headTrace)
            }
            visited.insert(vertex)
            heads.removeValue(forKey: vertex)
            if isEnd(vertex) {
                return (minDistance, headTrace)
            }
        }
        return nil
    }
    
    return nextResult()
}
