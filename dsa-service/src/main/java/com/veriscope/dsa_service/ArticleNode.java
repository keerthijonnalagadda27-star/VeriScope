package com.veriscope.dsa_service;

public class ArticleNode {
    private String domain;
    private String title;
    private String url;
    private String publishedAt;
    private String source;
    private boolean isOrigin;

    public ArticleNode(String domain, String title, String url, String publishedAt, String source, boolean isOrigin) {
        this.domain = domain;
        this.title = title;
        this.url = url;
        this.publishedAt = publishedAt;
        this.source = source;
        this.isOrigin = isOrigin;
    }
    public String getDomain() {
        return domain;
    }
    public String getTitle() {
        return title;
    }
    public String getUrl() {
        return url;
    }
    public String getPublishedAt() {
        return publishedAt;
    }
    public String getSource() {
        return source;
    }
    public boolean isOrigin() {
        return isOrigin;
    }

}


