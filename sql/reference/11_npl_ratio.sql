-- Non-performing loans and advances ratio: column 0060 over column 0010 of row 0070.

CREATE OR REPLACE VIEW npl_ratio AS
SELECT CAST(n.GRSS_CRRYNG_AMNT / NULLIF(d.GRSS_CRRYNG_AMNT, 0) AS DECIMAL(38,12)) AS NPL_RATIO
FROM f_18_00_a_r0070_c0060 AS n
CROSS JOIN f_18_00_a_r0070_c0010 AS d;
