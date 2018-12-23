create table t_music_list(
  id integer primary key autoincrement,
  name text  not null, -- 歌单名
  play_count integer  not null, -- 播放次数
  created text  not null, -- 创建时间, yyyy-mm-dd
  isDeleted int default 0 check ( isDeleted = 1 or isDeleted =0 ) --是否被删除, 1已被删除, 0未被删除
);

create table t_music (
  id integer primary key autoincrement,
  mlid integer not null, --关联的歌单id
  path text not null, --文件绝对路径
  size integer, --文件大小, 字节
  image text, --封面图片路径
  title text, --MP3 title
  artist text, --MP3 歌手名
  album text, --MP3 专辑名
  duration integer --MP3 时长, 秒
);

insert into t_music_list values (1, 'test1', 12, '1980-12-12', 0);
insert into t_music_list values (2, 'test22', 1212, '1881-12-12', 0);
insert into t_music_list values (3, 'test333', 1122, '2008-12-18', 0);


insert into t_music values (null, 1, '/path/a.mp3', 20000, '/image/1.png', 'title1', 'artist1', 'album1', '340');
insert into t_music values (null, 2, '/path/a.mp3', 20000, '/image/1.png', 'title1', 'artist1', 'album1', '340');
insert into t_music values (null, 3, '/path/a.mp3', 20000, '/image/1.png', 'title1', 'artist1', 'album1', '340');