# ------------------------------------------------------------------------------
# SETUP
if not DATA_PATH.exists():
    DATA_PATH.mkdir(parents=True)

if not Path(WORKLOG_FILE).exists():
    with Path(WORKLOG_FILE).open(mode='w', encoding='utf8') as f:
        f.write('date;action;info\n')
