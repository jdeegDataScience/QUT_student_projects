const options = require('./knexfile.js');
const knex = require('knex')(options);

async function main() {
    // create table 'users'
    // with a primary key using 'increments()'
    knex.schema.createTable('users', function (table) {
        table.primary('email', {constraintName: 'users_pk_email'});
        table.increments('userId');
        table.string('email').unique({deferrable: 'not deferrable'}).notNullable();
        table.string('hash', 60).notNullable();
        table.string('firstName');
        table.string('lastName');
        table.date('dob');
    });

    knex.schema.createTable('usersBLtokens', function (table) {
        table.primary('email', {constraintName: 'usersBLtokens_pk_email'});
        table.string('email').unique({deferrable: 'not deferrable'}).notNullable();
        table.string('BLfrom').notNullable();
    });

    knex.schema.createTable('videos', function (table) {
        table.primary('videoId', {constraintName: 'videos_pk_videoId'});
        table.string('videoId').unique({deferrable: 'not deferrable'}).notNullable();
        table.integer('userId').notNullable();
        table.string('title', 235).notNullable();
        table.string('thumbnail').notNullable();
        table.integer('length').notNullable();
        table.timestamp('ts').defaultTo(knex.fn.now());
    });
}

main();