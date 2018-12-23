create table t_music_list(
  id integer primary key autoincrement,
  name text comment '歌单名',
  play_count integer comment '播放次数',
  created text comment '创建时间, yyyy-mm-dd'
);

create table t_music (
  id integer primary key autoincrement,
  mlid integer comment '关联的歌单id',
  path text comment '文件绝对路径',
  size integer comment '文件大小, 字节',
  image text comment '封面图片路径',
  title text comment 'MP3 title',
  artist text comment 'MP3 歌手名',
  album text comment 'MP3 专辑名',
  duration integer comment 'MP3 时长, 秒'
);

insert into t_music_list values (1, 'test1', 12, '1980-12-12');
insert into t_music_list values (2, 'test22', 1212, '1881-12-12');
insert into t_music_list values (3, 'test333', 1122, '2008-12-18');


insert into t_music values (null, 1, '/path/a.mp3', 20000, '/image/1.png', 'title1', 'artist1', 'album1', '340');
insert into t_music values (null, 2, '/path/a.mp3', 20000, '/image/1.png', 'title1', 'artist1', 'album1', '340');
insert into t_music values (null, 3, '/path/a.mp3', 20000, '/image/1.png', 'title1', 'artist1', 'album1', '340');