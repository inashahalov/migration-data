-- Таблица: us_states
CREATE TABLE [us_states] (
  [state_id] NVARCHAR(MAX) NOT NULL,
  [state_name] NVARCHAR(100) NULL,
  [state_abbr] NVARCHAR(2) NULL,
  [state_region] NVARCHAR(50) NULL,
  CONSTRAINT [PK_us_states] PRIMARY KEY ([state_id])
);

-- Таблица: customers
CREATE TABLE [customers] (
  [customer_id] NVARCHAR(MAX) NOT NULL,
  [company_name] NVARCHAR(40) NOT NULL,
  [contact_name] NVARCHAR(30) NULL,
  [contact_title] NVARCHAR(30) NULL,
  [address] NVARCHAR(60) NULL,
  [city] NVARCHAR(15) NULL,
  [region] NVARCHAR(15) NULL,
  [postal_code] NVARCHAR(10) NULL,
  [country] NVARCHAR(15) NULL,
  [phone] NVARCHAR(24) NULL,
  [fax] NVARCHAR(24) NULL,
  CONSTRAINT [PK_customers] PRIMARY KEY ([customer_id])
);

-- Таблица: orders
CREATE TABLE [orders] (
  [order_id] NVARCHAR(MAX) NOT NULL,
  [customer_id] NVARCHAR(MAX) NULL,
  [employee_id] NVARCHAR(MAX) NULL,
  [order_date] DATE NULL,
  [required_date] DATE NULL,
  [shipped_date] DATE NULL,
  [ship_via] NVARCHAR(MAX) NULL,
  [freight] NVARCHAR(MAX) NULL,
  [ship_name] NVARCHAR(40) NULL,
  [ship_address] NVARCHAR(60) NULL,
  [ship_city] NVARCHAR(15) NULL,
  [ship_region] NVARCHAR(15) NULL,
  [ship_postal_code] NVARCHAR(10) NULL,
  [ship_country] NVARCHAR(15) NULL,
  CONSTRAINT [PK_orders] PRIMARY KEY ([order_id])
);

-- Таблица: employees
CREATE TABLE [employees] (
  [employee_id] NVARCHAR(MAX) NOT NULL,
  [last_name] NVARCHAR(20) NOT NULL,
  [first_name] NVARCHAR(10) NOT NULL,
  [title] NVARCHAR(30) NULL,
  [title_of_courtesy] NVARCHAR(25) NULL,
  [birth_date] DATE NULL,
  [hire_date] DATE NULL,
  [address] NVARCHAR(60) NULL,
  [city] NVARCHAR(15) NULL,
  [region] NVARCHAR(15) NULL,
  [postal_code] NVARCHAR(10) NULL,
  [country] NVARCHAR(15) NULL,
  [home_phone] NVARCHAR(24) NULL,
  [extension] NVARCHAR(4) NULL,
  [photo] NVARCHAR(MAX) NULL,
  [notes] NVARCHAR(MAX) NULL,
  [reports_to] NVARCHAR(MAX) NULL,
  [photo_path] NVARCHAR(255) NULL,
  CONSTRAINT [PK_employees] PRIMARY KEY ([employee_id])
);

-- Таблица: shippers
CREATE TABLE [shippers] (
  [shipper_id] NVARCHAR(MAX) NOT NULL,
  [company_name] NVARCHAR(40) NOT NULL,
  [phone] NVARCHAR(24) NULL,
  CONSTRAINT [PK_shippers] PRIMARY KEY ([shipper_id])
);

-- Таблица: products
CREATE TABLE [products] (
  [product_id] NVARCHAR(MAX) NOT NULL,
  [product_name] NVARCHAR(40) NOT NULL,
  [supplier_id] NVARCHAR(MAX) NULL,
  [category_id] NVARCHAR(MAX) NULL,
  [quantity_per_unit] NVARCHAR(20) NULL,
  [unit_price] NVARCHAR(MAX) NULL,
  [units_in_stock] NVARCHAR(MAX) NULL,
  [units_on_order] NVARCHAR(MAX) NULL,
  [reorder_level] NVARCHAR(MAX) NULL,
  [discontinued] INT NOT NULL,
  CONSTRAINT [PK_products] PRIMARY KEY ([product_id])
);

-- Таблица: order_details
CREATE TABLE [order_details] (
  [order_id] NVARCHAR(MAX) NOT NULL,
  [product_id] NVARCHAR(MAX) NOT NULL,
  [unit_price] NVARCHAR(MAX) NOT NULL,
  [quantity] NVARCHAR(MAX) NOT NULL,
  [discount] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_order_details] PRIMARY KEY ([order_id], [product_id])
);

-- Таблица: categories
CREATE TABLE [categories] (
  [category_id] NVARCHAR(MAX) NOT NULL,
  [category_name] NVARCHAR(15) NOT NULL,
  [description] NVARCHAR(MAX) NULL,
  [picture] NVARCHAR(MAX) NULL,
  CONSTRAINT [PK_categories] PRIMARY KEY ([category_id])
);

-- Таблица: suppliers
CREATE TABLE [suppliers] (
  [supplier_id] NVARCHAR(MAX) NOT NULL,
  [company_name] NVARCHAR(40) NOT NULL,
  [contact_name] NVARCHAR(30) NULL,
  [contact_title] NVARCHAR(30) NULL,
  [address] NVARCHAR(60) NULL,
  [city] NVARCHAR(15) NULL,
  [region] NVARCHAR(15) NULL,
  [postal_code] NVARCHAR(10) NULL,
  [country] NVARCHAR(15) NULL,
  [phone] NVARCHAR(24) NULL,
  [fax] NVARCHAR(24) NULL,
  [homepage] NVARCHAR(MAX) NULL,
  CONSTRAINT [PK_suppliers] PRIMARY KEY ([supplier_id])
);

-- Таблица: region
CREATE TABLE [region] (
  [region_id] NVARCHAR(MAX) NOT NULL,
  [region_description] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_region] PRIMARY KEY ([region_id])
);

-- Таблица: territories
CREATE TABLE [territories] (
  [territory_id] NVARCHAR(20) NOT NULL,
  [territory_description] NVARCHAR(MAX) NOT NULL,
  [region_id] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_territories] PRIMARY KEY ([territory_id])
);

-- Таблица: employee_territories
CREATE TABLE [employee_territories] (
  [employee_id] NVARCHAR(MAX) NOT NULL,
  [territory_id] NVARCHAR(20) NOT NULL,
  CONSTRAINT [PK_employee_territories] PRIMARY KEY ([employee_id], [territory_id])
);

-- Таблица: customer_demographics
CREATE TABLE [customer_demographics] (
  [customer_type_id] NVARCHAR(MAX) NOT NULL,
  [customer_desc] NVARCHAR(MAX) NULL,
  CONSTRAINT [PK_customer_demographics] PRIMARY KEY ([customer_type_id])
);

-- Таблица: customer_customer_demo
CREATE TABLE [customer_customer_demo] (
  [customer_id] NVARCHAR(MAX) NOT NULL,
  [customer_type_id] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_customer_customer_demo] PRIMARY KEY ([customer_id], [customer_type_id])
);

