create table comments
(
    id          varchar(32)  not null
        primary key,
    userName    varchar(255) null,
    goal        int          null,
    publishDate varchar(255) null comment '评论时间',
    message     text         null,
    other       text         null
);

create table hotel
(
    id          varchar(32)  not null
        primary key,
    hotel_name  varchar(255) null,
    comment_num varchar(255) null,
    price       varchar(255) null,
    hotel_rank  varchar(255) null,
    hotel_score varchar(255) null,
    img         text         null,
    keywords    text         null
);

create table site
(
    other       text          null,
    site_name   varchar(255)  null comment '景点名称',
    brief       text          null comment '景点的介绍',
    imgs        text          null comment '图片，字典形式保存
',
    site        varchar(255)  null comment '景点具体位置',
    id          varchar(32)   not null
        primary key,
    site_type   int default 0 null,
    img         text          null,
    num_comment varchar(255)  null,
    `rank`      varchar(255)  null,
    num_ginfo   varchar(10)   null
);

create table siteandcomment
(
    id         int auto_increment
        primary key,
    site_id    varchar(255) not null,
    comment_id varchar(255) null
);

create table user
(
    id          int auto_increment
        primary key,
    username    varchar(255)                        not null,
    password    varchar(255)                        null,
    update_time timestamp default CURRENT_TIMESTAMP null
);

