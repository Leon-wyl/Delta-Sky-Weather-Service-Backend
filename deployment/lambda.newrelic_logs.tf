module "newrelic_log_ingestion" {
  source             = "github.com/newrelic/aws-log-ingestion"
  nr_license_key     = "{{b43497e898fe8785a353d22f8125c7fd39cdNRAL}}"
  nr_tags = "NR function"
}