DROP DATABASE IF EXISTS software;
CREATE DATABASE software;
Use software;
CREATE TABLE Users(
	user_id VARCHAR(255) NOT NULL UNIQUE,
    fullname VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL 
);

CREATE TABLE Documents(
	document_id VARCHAR(255) PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP DEFAULT current_timestamp,
    file_path VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
Use software;
DROP TABLE IF EXISTS Printers;
CREATE TABLE Printers(
	printer_id VARCHAR(255) PRIMARY KEY,
    printer_name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    supports_color BOOL NOT NULL,
    supports_duplex BOOL NOT NULL,
    max_paper_size VARCHAR(255) NOT NULL,
    printer_status VARCHAR(255) DEFAULT ''
);
Use software;
DROP TABLE IF EXISTS PrintSettings;
CREATE TABLE PrintSettings(
	setting_id VARCHAR(255) PRIMARY KEY,
    document_id VARCHAR(255) NOT NULL,
    color BOOL NOT NULL,
    copies INT NOT NULL,
    duplex BOOL NOT NULL,
    paper_size VARCHAR(255) NOT NULL,
    time_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (document_id) REFERENCES Documents(document_id)
);

Use software;
DROP PROCEDURE IF EXISTS InsertSettings;
DROP PROCEDURE IF EXISTS GetSettings;
DROP PROCEDURE IF EXISTS UpdateSettings;
DELIMITER //
USE software //

CREATE PROCEDURE InsertSettings(
    IN p_setting_id VARCHAR(255),
    IN p_document_id VARCHAR(255),
    IN p_color BOOL,
    IN p_copies INT,
    IN p_duplex BOOL,
    IN p_paper_size VARCHAR(255)
)
BEGIN
    -- Check if the setting ID already exists in the PrintSettings table
    IF EXISTS (SELECT 1 FROM PrintSettings WHERE setting_id = p_setting_id) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Setting ID already exists.';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM Documents WHERE document_id = p_document_id) THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: No Document ID exists.';
    END IF;

    -- If all checks pass, insert the new settings into the PrintSettings table
    INSERT INTO PrintSettings (
        setting_id,
        document_id,
        color,
        copies,
        duplex,
        paper_size
    )
    VALUES (
        p_setting_id,
        p_document_id,
        p_color,
        p_copies,
        p_duplex,
        p_paper_size
    );

    -- Return a success message
    SELECT 'Settings inserted successfully' AS message;
END //

CREATE PROCEDURE GetSettings
(	
	IN p_document_id VARCHAR(255)
)
BEGIN
	IF NOT EXISTS (SELECT 1 FROM PrintSettings WHERE document_id = p_document_id) THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: No Document ID exists.';
    END IF;
    SELECT * FROM PrintSettings
    WHERE document_id = p_document_id;
END //

CREATE PROCEDURE UpdateSettings 
(
	IN p_document_id VARCHAR(255),
    IN p_color BOOL,
    IN p_copies INT,
    IN p_duplex BOOL,
    IN p_paper_size VARCHAR(255)
)
BEGIN 
	DECLARE v_latest_setting_id VARCHAR(255);
	IF NOT EXISTS (SELECT 1 FROM PrintSettings WHERE document_id = p_document_id) THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: No Document ID exists.';
    END IF;
    

    -- Find the latest setting for the given document_id
    SELECT setting_id
    INTO v_latest_setting_id
    FROM PrintSettings
    WHERE document_id = p_document_id
    ORDER BY time_updated DESC
    LIMIT 1;
    IF v_latest_setting_id IS NOT NULL THEN
		UPDATE PrintSettings 
		SET 
			color = COALESCE(p_color, color),
			copies = COALESCE(p_copies, copies),
			duplex = COALESCE(p_duplex, duplex),
			paper_size = COALESCE(p_paper_size, paper_size),
			time_updated = CURRENT_TIMESTAMP
		WHERE document_id = p_document_id AND setting_id = v_latest_setting_id;
	END IF;
END //
DELIMITER ;