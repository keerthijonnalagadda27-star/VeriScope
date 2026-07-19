package com.veriscope.dsa_service;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@CrossOrigin(origins = "*")
@RequestMapping("/dsa")

public class DsaController {
    @GetMapping("/health")
    public Map<String,String>health(){
        Map<String,String>response=new HashMap<>();
        response.put("status","VeriScope DSA service is running");
        response.put("service","SpreadGraph + BFS");
        return response;
    }
    @PostMapping("/spread")
    public Map<String,Object> buildSpreadGraph(@RequestBody Map<String,Object> body){
        List<Map<String,Object>>articles=
                (List<Map<String,Object>>)body.get("articles");

        if(articles==null || articles.isEmpty()){
            Map<String,Object>empty=new HashMap<>();
            empty.put("nodes",new ArrayList<>());
            empty.put("edges",new ArrayList<>());
            empty.put("spread_path",new ArrayList<>());
            empty.put("origin",null);
            return empty;
        }
        SpreadGraph graph=new SpreadGraph();

        for(int i=0;i<articles.size();i++){
            Map<String,Object> article=articles.get(i);

            ArticleNode node=new ArticleNode(
                    (String) article.get("domain"),
                    (String) article.get("title"),
                    (String) article.get("url"),
                    (String) article.get("publishedAt"),
                    (String) article.get("source"),
                    i==0

            );
            graph.addNode(node);
        }

        String originDomain=(String) articles.get(0).get("domain");
        for(int i=1;i<articles.size();i++){
            String targetDomain=(String) articles.get(i).get("domain");
            graph.addEdge(originDomain,targetDomain);
        }

        List<String>spreadPath=graph.bfsSpreadPath(originDomain);

        List<Map<String,Object>>nodeList=new ArrayList<>();
        for(ArticleNode node:graph.getNodes().values()){
            Map<String,Object>nodeMap=new HashMap<>();
            nodeMap.put("id", node.getDomain());
            nodeMap.put("label", node.getSource());
            nodeMap.put("domain", node.getDomain());
            nodeMap.put("published_at", node.getPublishedAt());
            nodeMap.put("url", node.getUrl());
            nodeMap.put("is_origin", node.isOrigin());
            nodeList.add(nodeMap);
        }

        List<Map<String,String>>edgeList=new ArrayList<>();

        for(Map.Entry<String,List<String>>entry:
            graph.getAdjacencyList().entrySet()){
            for(String target:entry.getValue()){
                Map<String,String>edge=new HashMap<>();
                edge.put("from", entry.getKey());
                edge.put("to", target);
                edgeList.add(edge);

            }
        }

        Map<String,Object>originInfo=new HashMap<>();
        originInfo.put("domain",articles.get(0).get("domain"));
        originInfo.put("source",articles.get(0).get("source"));
        originInfo.put("published_at",articles.get(0).get("publishedAt"));
        originInfo.put("url",articles.get(0).get("url"));


        Map<String,Object>response=new HashMap<>();
        response.put("nodes",nodeList);
        response.put("edges",edgeList);
        response.put("spread_path",spreadPath);
        response.put("origin",originInfo);
        response.put("total_nodes",nodeList.size());
        return response;

    }

}
