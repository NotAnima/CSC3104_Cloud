CREATE TABLE model (
    id SERIAL PRIMARY KEY,
    model BYTEA NOT NULL, -- Store pickle file as binary data
    datetime TIMESTAMP NOT NULL
);
