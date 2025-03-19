CREATE TABLE IF NOT EXISTS quotes (
    quote VARCHAR(255) NOT NULL, 
    author VARCHAR(100) NOT NULL
);

INSERT INTO quotes (quote, author) VALUES ('In the middle of every difficulty lies opportunity.', 'Albert Einstein');
INSERT INTO quotes (quote, author) VALUES ('Houston, we have a problem.', 'Jim Lovell'); 
INSERT INTO quotes (quote, author) VALUES ('To be or not to be, that is the question.', 'William Shakespeare');