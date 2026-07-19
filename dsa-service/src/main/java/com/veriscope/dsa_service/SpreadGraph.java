package com.veriscope.dsa_service;
import java.util.*;

public class SpreadGraph {
    private HashMap<String,ArticleNode>nodes;
    private HashMap<String,List<String>>adjacencyList;

    public SpreadGraph(){
        nodes = new HashMap<>();
        adjacencyList = new HashMap<>();
    }
    public void addNode(ArticleNode node){
        nodes.put(node.getDomain(),node);
        adjacencyList.put(node.getDomain(),new ArrayList<>());
    }
    public void addEdge(String fromDomain,String toDomain){
        if(adjacencyList.containsKey(fromDomain)){
            adjacencyList.get(fromDomain).add(toDomain);
        }
    }

    public List<String>bfsSpreadPath(String originDomain){

        List<String>spreadPath = new ArrayList<>();

        if(!nodes.containsKey(originDomain)){
            return spreadPath;

        }
        Set<String>visited=new HashSet<>();

        Queue<String>queue=new LinkedList<>();

        queue.add(originDomain);
        visited.add(originDomain);

        while(!queue.isEmpty()){
            String current=queue.poll();

            spreadPath.add(current);

            List<String>neighbours=adjacencyList.get(current);
            if(neighbours!=null){
                for(String neighbour:neighbours){
                    if(!visited.contains(neighbour)){
                        visited.add(neighbour);
                        queue.add(neighbour);
                    }
                }
            }
        }
        return spreadPath;

    }
    public HashMap<String,ArticleNode> getNodes(){
        return nodes;
    }
    public HashMap<String,List<String>>getAdjacencyList(){
        return adjacencyList;
    }


    
}
