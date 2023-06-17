DROP DATABASE IF EXISTS app;
CREATE DATABASE app;
USE app;

CREATE TABLE IF NOT EXISTS `users` (
    `traq_id` varchar(255) NOT NULL,
    `total_point` int(11) DEFAULT 0,
    `github_id` varchar(255) DEFAULT NULL,
    `atcoder_id` varchar(255) DEFAULT NULL,
    `traq_point_type` varchar(255) DEFAULT NULL,
    `github_point_type` varchar(255) DEFAULT NULL,
    `atcoder_point_type` varchar(255) DEFAULT NULL,
    `github_total_contributions` int(11) DEFAULT 0,
    `traq_total_posts` int(11) DEFAULT 0,
    `atcoder_total_ac` int(11) DEFAULT 0,
    PRIMARY KEY (`traq_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `trees` (
    `tree_id` int(11) NOT NULL AUTO_INCREMENT,
    `traq_id` varchar(255) NOT NULL,
    `branch_count` int(11) DEFAULT NULL,
    PRIMARY KEY (`tree_id`),
    KEY `traq_id` (`traq_id`),
    CONSTRAINT `trees_ibfk_1` FOREIGN KEY (`traq_id`) REFERENCES `users` (`traq_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `leaves` (
    `tree_id` int(11) NOT NULL,
    `leaf_id` int(11) NOT NULL,
    `position_x` int(11) DEFAULT NULL,
    `position_y` int(11) DEFAULT NULL,
    `color` varchar(255) DEFAULT NULL,
    `size` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`tree_id`,`leaf_id`),
    CONSTRAINT `leaves_ibfk_1` FOREIGN KEY (`tree_id`) REFERENCES `trees` (`tree_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
