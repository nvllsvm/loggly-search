# loggly-search
A CLI for Loggly search

## Installation
```
pip install loggly-search
```

## Configuration
You'll need both your account subdomain (ex. `myaccount` of `myaccount.loggly.com`) 
and an [API token](https://documentation.solarwinds.com/en/success_center/loggly/content/admin/token-based-api-authentication.htm) to use this tool.
Both of these can then be passed via the `--subdomain` and `--token` parameters or
through the `LOGGLY_SUBDOMAIN` and `LOGGLY_TOKEN` environment variables.

```
loggly-search --subdomain myaccount --token abcxyz
```

## Usage Examples
```
loggly-search --from=-7d CRITERIA
```

```
loggly-search --from '2022-05-17T08:00:00.000-04:00' --to '2022-05-17T10:00:00.000-04:00' CRITERIA
```
