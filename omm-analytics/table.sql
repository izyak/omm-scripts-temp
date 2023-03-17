# create
#     database `omm-analytics`;
use
    `omm-analytics`;
CREATE TABLE `omm_staking_amount`
(
    `staking`         float   DEFAULT NULL,
    `unstaking`       float   DEFAULT NULL,
    `cancelUnstaking` float   DEFAULT NULL,
    `timestamp`       int(11) DEFAULT NULL,
    `_index`          int(11) NOT NULL,
    PRIMARY KEY (`_index`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

CREATE TABLE `omm_staking_stats`
(
    `staking`         int(11) DEFAULT NULL,
    `unstaking`       int(11) DEFAULT NULL,
    `cancelUnstaking` int(11) DEFAULT NULL,
    `timestamp`       int(11) DEFAULT NULL,
    `_index`          int(11) NOT NULL,
    PRIMARY KEY (`_index`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

CREATE TABLE `reserve_amount`
(
    `_index`    int(11)     NOT NULL,
    `timestamp` int(11) DEFAULT NULL,
    `deposit`   float   DEFAULT NULL,
    `borrow`    float   DEFAULT NULL,
    `repay`     float   DEFAULT NULL,
    `redeem`    float   DEFAULT NULL,
    `reserve`   varchar(10) NOT NULL,
    PRIMARY KEY (`_index`, `reserve`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

CREATE TABLE `reserve_stats`
(
    `_index`         int(11)     NOT NULL,
    `timestamp`      int(11) DEFAULT NULL,
    `deposit`        int(11) DEFAULT NULL,
    `borrow`         int(11) DEFAULT NULL,
    `repay`          int(11) DEFAULT NULL,
    `redeem`         int(11) DEFAULT NULL,
    `unique_address` int(11) DEFAULT NULL,
    `reserve`        varchar(10) NOT NULL,
    PRIMARY KEY (`_index`, `reserve`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

CREATE TABLE `timestamp_history`
(
    `_key`      varchar(10) NOT NULL,
    `timestamp` bigint(20) DEFAULT NULL,
    PRIMARY KEY (`_key`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;


insert into timestamp_history(`_key`, `timestamp`)
values ("OMM", 1638316800000000),
       ("RESERVE", 1638316800000000);

create table omm_utilization_rates
(
    `reserve`             varchar(20),
    `timestamp`           int,
    `total_borrows`       float NOT NULL,
    `total_borrows_usd`   float NOT NULL,
    `total_liquidity`     float NOT NULL,
    `total_liquidity_usd` float NOT NULL,
    `utilization_rate`    float NOT NULL,
    primary key (`reserve`, `timestamp`)
);


CREATE TABLE `bomm_stats`
(
    `user`   varchar(42) NOT NULL,
    `amount` float   DEFAULT NULL,
    `expire` int(10) DEFAULT NULL,
    PRIMARY KEY (`user`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

CREATE TABLE `bomm_users`
(
    `user`      varchar(42) NOT NULL,
    `createdAt` TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (`user`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

CREATE VIEW bomm_stats_view AS
SELECT from_unixtime(expire, '%Y %D %M') AS unlock_date,
       sum(amount)                       AS totalOMMLocked,
       count(user)                       AS numberOfUsers
FROM bomm_stats
GROUP BY expire
ORDER by expire ASC;

CREATE VIEW bomm_users_view AS
SELECT group_concat(user SEPARATOR ','),
       count(1)                  as count,
       from_unixtime((UNIX_TIMESTAMP(createdAt) div (86400 * 7)) * (86400 * 7),
                     '%Y %D %M') as dateFrom,
       from_unixtime((UNIX_TIMESTAMP(createdAt) div (86400 * 7) + 1) * (86400 * 7)-86400,
                     '%Y %D %M') as dateTo
FROM bomm_users
group by dateTo
ORDER by STR_TO_DATE(dateTo,'%Y %D %M') DESC;