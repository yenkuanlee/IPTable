create foreign table student (
        TSID bigint,
        Name text,
        school text,
        age int,
        StudentID text
    ) server ipserver options (
          table_name 'student',
          fhash 'QmW5pgzxDJ8ao2eqKrnVse2idsABDikf55FYx4BBDj25ga'
    );
