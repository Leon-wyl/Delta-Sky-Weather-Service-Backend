module "newrelic_log_ingestion" {
  source             = "github.com/newrelic/aws-log-ingestion"
  nr_license_key     = "{{b43497e898fe8785a353d22f8125c7fd39cdNRAL}}"
  nr_tags = "NR function"
  service_name = "SENG3011_[F14A_DELTA]_[NR_func]_newrelic_log_ingestion"
}