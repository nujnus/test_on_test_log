test() {
log_file="${1}_test"
expect_file="${1}_expect"

nightwatch  --test ./nightwatch_job.js --testcase $2

curl -i -H "Content-Type: application/json;charset=UTF-8" -X POST -d "{\"target_filename\":\"${log_file}\"}" http://127.0.0.1:5002/manage/tofile

curl -i -H "Content-Type: application/json;charset=UTF-8" -X POST -d "{\"target_filename\":\"${log_file}\"}" http://127.0.0.1:5002/manage/tofile_data

curl -i  http://127.0.0.1:5002/manage/clear

logtest cmp  ${log_file} ${expect_file} $2 {{history_cwd}} {{nightwatch_result}}
}

cd {{history_cwd}}
{{cmd}}
