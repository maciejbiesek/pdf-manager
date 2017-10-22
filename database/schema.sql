drop table if exists document;
create table document (
  id integer primary key autoincrement,
  filename text not null,
  pages int not null
);

drop table if exists content;
create table content (
  id integer primary key autoincrement,
  page_number integer not null,
  content text not null,
  document_id integer not null,
  foreign key(document_id) references documents(id)
);
