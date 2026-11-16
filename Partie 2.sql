CREATE TABLE `users` (
  `id` integer PRIMARY KEY,
  `first_name` varchar(255),
  `last_name` varchar(255),
  `email` varchar(255),
  `phone` varchar(255),
  `address` text
);

CREATE TABLE `products` (
  `id` integer PRIMARY KEY,
  `title` varchar(255),
  `description` text,
  `price` decimal,
  `category` varchar(255),
  `brand` varchar(255),
  `attributes` json
);

CREATE TABLE `carts` (
  `id` integer PRIMARY KEY,
  `user_id` integer NOT NULL,
  `total` decimal,
  `total_products` integer,
  `total_quantity` integer
);

CREATE TABLE `cart_items` (
  `cart_id` integer NOT NULL,
  `product_id` integer NOT NULL,
  `quantity` integer NOT NULL,
  `unit_price` decimal,
  PRIMARY KEY (`cart_id`, `product_id`)
);

ALTER TABLE `carts` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `cart_items` ADD FOREIGN KEY (`cart_id`) REFERENCES `carts` (`id`);

ALTER TABLE `cart_items` ADD FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);
