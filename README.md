# Firefly III bank import

Python programm/library for automatic import of transactions from different bankaccounts into Firefly III.

- [Firefly III bank import](#firefly-iii-bank-import)
  - [Supported Banks](#supported-banks)
    - [Extend Bank support](#extend-bank-support)
  - [Config](#config)
    - [Firefly](#firefly)
    - [Banks](#banks)
      - [N26](#n26)
  - [CLI](#cli)
  - [Python Module](#python-module)
    - [Config](#config-1)
    - [FireflyAPI](#fireflyapi)
    - [Loader](#loader)
    - [Importer](#importer)
  - [Known Issues](#known-issues)
    - [Timezones](#timezones)
    - [Transactions between N26 spaces](#transactions-between-n26-spaces)
    - [N26 Transaction limit](#n26-transaction-limit)

## Supported Banks

- [N26](https://n26.com/de-de)<sup>*</sup>


><sup>*</sup> Realized using an inofficial API. Use with caution.

### Extend Bank support

If you want to create support for a new bank account you need to create a new loader class as well as a new config class for this type of account (See [Python Module](#python-module) for a complete explanation of the class structure).

The config class should inherit from `config.BankConfig` and should contain the attributes necessary to configure access to this type of account. Make sure, to extend the `if-else` statement in `config.BankConfig.from_type()` as well as `config.BANK_TYPES` with the identifier of the new account type.

Next a new loader should be create which has to inherit from `loader.BaseLoader`. This is, where all the logic will be located. Write a method `load_transaction(start: datetime, end: datetime) which loads all transactions in the given timeframe and converts them into a `Transaction` object.

In the end make sure to also update the `if-else` statement in the `_init_loader` function of the `cli` module with the identifier of the new account type. Without this the new bank account will not work in the cli.

**Finished!** You can now add the config of your bank account to the `f3i.config.toml` and you are ready to go.

## Config

The Firefly importer uses a `.toml` file for configuration with the folowing structure. A minimal preset to get started with is also located in the root folder of this project.

### Firefly

The firefly config includes the address of the firefly instance as well as a personal access token. The token has to be generated in Firefly III under *Options > Profile > OAuth*.

*Example:*
```toml
[firefly]
host="https://firefly/host/adress"
token="private_access_token"
```

### Banks

The banks config is a list of configurations for different accounts. Every account configuration needs at least a `type` and a `name`. Other values/options are defined by the given account type.

The `type` identifies which type of account this config is used for (see [Supported Banks](#supported-banks)) and the `name` is the name of the equivalent account in Firefly III.

*Example:*
```toml
[[banks]]
type="n26"
name="My Private Account"
...

[[banks]]
type="n26"
name="My Business Account"
...
```

#### N26

The N26 account configuration takes the folowing values: `username`, `password`, `device_token`, `mfa_type` and `store_login_data`

The `username` and `password` are the login informations to your N26 account. Be very carefull with this information

The `device_token` is a custom UUID which is used to identify your device. You can create it yourself using python:

```bash
python -c 'import uuid; print(uuid.uuid4())'
```

With the `mfa_type` you decide with wich type of MFA the login of the program should be verified. You can choose between **'app'** and **'sms'**.

In order to avoid MFA every time the script is executed the login/token information can be saved on device. The option `store_login_data` decides if this is the case or not.
> The login information usually only remains valid for some minutes

*Example*
```toml
[[banks]]
type="n26"
name="My Private Account"
username="some_email@domain.com"
password="password"
device_token="394d3be6-4fcf-452f-b089-a098b00c7457"
mfa_type="app"
store_login_data=true
```

## CLI

The CLI can be used to just import transactions from a given timeframe once or use the auto import to repeatedly import all transactions since the last time the script was executed.

The one time import can be executed by providing a `--from` and a optional `--to` date (and time) in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.

```bash
f3i --from 2022-03-10 --to 2022-04-10T10:30
```
When no `--to` argument is provide the script automatically imports all transactions up to the current date.

```bash
f3i --from 2022-10-20
```

When niether a `--from` and a `--to` date is provided the auto import is triggerd. This part of the script saves the last time it was executed and imports all transactions since this timestamp. The first time the auto import is executed no import will take place and it will just save the current date as the last execution time.

```bash
f3i
```

If you want to reset the last execution timestamp of the auto importer use the argument `--reset`.

```bash
f3i --reset
```

By default the program looks for this file at `./` and then `~/`. Aditionally the path to a config file can be added when executing the cli using the `--config` option.

```bash
f3i --from 2022-06-02 --config ./path/to/config.toml
```

## Python Module

Aside from the CLI the `firefly_iii_import` library can be used directly in a python program.

It provides an `FireflyAPI` abstraction layer for creating transactions and a set of loaders for different bank accounts. For easy import and configuration there is also the `Importer` class as well as some config classes.

### Config

The `Config` class provides an easy and consistent way to interact with the `firefly_iii_import` configuration.
It can be used to load a config from a given path.

```py
from firefly_iii_import import Config

Config.load("path/to/config.toml")
```

Alternatively the `Config` class can be initialized directly with a dictionary including the necessary information.

```py
from firefly_iii_import import Config

Config(dict(
  firefly=dict(
    host="https://firefly/host/adress"
    token="private_access_token"
  ),
  banks=[
    dict(
      type="n26"
      name="My Private Account"
      username="some_email@domain.com"
      password="password"
      device_token="394d3be6-4fcf-452f-b089-a098b00c7457"
      mfa_type="app"
      store_login_data=True
    )
  ]
))
```

The default path to the *f3i.config.toml* (if it was found) can be accessed using `DEFAULT_CONFIG_PATH`. If no file was found this variable is a empty string.

```py
from firefly_iii_import import DEFAULT_CONFIG_PATH
```

### FireflyAPI

The `FireflyAPI` class is a minimal abstraction layer for the Firefly III Api based on the [`firefly_iii_client`](https://github.com/ms32035/firefly-iii-client) library. It only provides a method to create a single `Transaction`.

```py
from firefly_iii_import import FireflyAPI, Transaction
from firefly_iii_client.model.transaction_type_property import TransactionTypeProperty

api = FireflyAPI("https://firefly/host/adress", "personal_access_token")
api.create_transaction(
  Transaction(
    amount=3,
    source="My Account",
    destination="Partner Account",
    date=datetime.now(),
    type=TransactionTypeProperty("withdrawal")
  )
)
```

### Loader

The `loader` module contains the different loading logic for all bank accounts. Each supported bank has it's own loader class based on `loader.BaseLoader`. Therefore they all provide a `load_transaction(start, end)` method. This method loads all transactions in the given timeframe and returns them as `list` of `Transaction` objects.

```py
from firefly_iii_import.loader import N26Loader
from firefly_iii_import import Transaction

loader = N26Loader(n26_account_config)
transactions: List[Transation] = loader.load_transactions(datetime.now() - timedelta(days=5), datetime.now())
```

### Importer

The `Importer` class provides a general interface to import transactions from different accounts into Firefly III. It provides a method for automatic import (`auto_import()`) as well as for import in a given timeframe (`run(start, end)`). The class also provides a method to reset the 'last_executed' timestamp for the auto import (`reset_auto_import`)

On initialization you ned to provide a list of `loader.BaseLoader` objects which are later used to load the transactions.

```py
from firefly_iii_import import Importer

importer = Importer(loaders, firefly_api)

importer.run(datetime.now() - timedelta(days=5), datetime.now())
importer.auto_import()
importer.reset()
```

## Known Issues

### Timezones

At the moment there is no handling of timezones when loading and creating transactions. This could cause some shifts in date and time during the import process. If you execute the script in the same timezone as your Firefly III instance is running and your bank accounts are registered there should be no problem

> N26 only provides a timestamp with the transaction but no timezone. From my limited testing the timestamp seems to be in the same timezone as the 'location' of the account.

### Transactions between N26 spaces

Transaction between N26 spaces are not handled in this importer. In general the N26 API only provides transactions between the main space and other spaces. Those usually occur in Firefly III with a source or destination called something like **'From {Space A} to {Space B}'** in the category **'Scellaneous'**.

The easiest workaround is to use Firefly III rules to change or delete those transactions.

### N26 Transaction limit

When loading transactions from a N26 account the API requires to limit the number of transactions to load. In the `N26Loader` this limit is set to `10000` which should be enough for most imports but you should be aware of this limit.
