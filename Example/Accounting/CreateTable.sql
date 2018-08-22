create foreign table accounting (
        TSID bigint,
        Adate text,
        item text,
        description text,
        twd int
    ) server ipserver options (
          table_name 'accounting'
    );
