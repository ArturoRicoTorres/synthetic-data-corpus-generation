# Over the counter (OTC) Derivative as a hedge (OTC_DRVTV_HDG_IL)

An Over the counter (OTC) Derivative as a hedge is an Over the counter (OTC) Derivative role where the Over
the counter (OTC) Derivative instrument acts as a hedge.

## Columns

| Column | Business name | Type | Key | Definition |
|---|---|---|---|---|
| `DT_RFRNC` | [Reference date](../../../shared/regulatory/glossary.md#reference-date) | DATE | PK | Reporting agents shall report credit data as recorded on the following reporting reference dates: (a) for monthly transmissions, on the last day of each month; (b) for quarterly transmissions, on the last day of March, June, September and December. |
| `RPRTNG_AGNT_ID` | [Reporting agent identifier](../../../shared/regulatory/glossary.md#reporting-agent-identifier) | VARCHAR(255) | PK | Reporting agent identifier |
| `ACCNTNG_CNSLDTN_LVL` | [Accounting consolidation level](../../../shared/regulatory/glossary.md#accounting-consolidation-level) | VARCHAR(255) | PK | Accounting consolidation level is the level on which the accounting is consolidated, Solo or group. |
| `ACCNTNG_STNDRD` | [Accounting standard](../../../shared/regulatory/glossary.md#accounting-standard) | VARCHAR(255) | PK | Accounting standard |
| `INSTRMNT_ID` | [Instrument identifier](../../../shared/regulatory/glossary.md#instrument-identifier) | VARCHAR(255) | PK | An identifier applied by the reporting agent to uniquely identify each instrument under a single contract. Each instrument must have one instrument identifier. This value will not change over time and cannot be used as the instrument identifier for any other instrument under the same contract. |
| `ACCNTNG_HDG_INDCTR` | [Accounting hedge indicator](../../../shared/regulatory/glossary.md#accounting-hedge-indicator) | VARCHAR(255) |  | An indicator specifying if the hedge is considered an accounting hedge or not. |

## Relationships

- belongs to [INSTRMNT_IL](INSTRMNT_IL.md) on `ACCNTNG_CNSLDTN_LVL` = `ACCNTNG_CNSLDTN_LVL`, `ACCNTNG_STNDRD` = `ACCNTNG_STNDRD`, `DT_RFRNC` = `DT_RFRNC`, `INSTRMNT_ID` = `INSTRMNT_ID`, `RPRTNG_AGNT_ID` = `RPRTNG_AGNT_ID`
  - BIRD relationship(s): ASS_OTC_DRVTV_INSTRMNT_OTC_DRVTV_HDG_60023_IL

## Code lists

### ACCNTNG_HDG_INDCTR: Accounting hedge indicator

| Code value | Code | Name |
|---|---|---|
| `ACCNTNG_HDG_INDCTR_1` | 1 | Accounting hedge |
| `ACCNTNG_HDG_INDCTR_2` | 2 | Not accounting hedge |
