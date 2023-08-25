import argparse
import datetime
from decimal import Decimal
import pytest
from acc import main


@pytest.mark.parametrize(
    "args, date, days",
    [
        (["date"], None, None),
        (["date", "2020-02-02"], datetime.date(2020, 2, 2), None),
        (["date", "--advance", "1"], None, main.daydelta(1)),
        (["date", "--advance"], None, main.daydelta(1)),
    ],
)
def test_date(args, date, days):
    assert main.parse_args(args) == argparse.Namespace(
        command="date", date=date, days=days
    )


@pytest.mark.parametrize(
    "args, ledger",
    [
        (["ledger"], None),
        (["ledger", "/tmp/foo"], main.Ledger("/tmp/foo")),
    ],
)
def test_ledger(args, ledger):
    assert main.parse_args(args) == argparse.Namespace(command="ledger", ledger=ledger)


@pytest.mark.parametrize(
    "args, command, amount, description",
    [
        (
            ["credit", "15", "--description", "orange"],
            "credit",
            Decimal("15.00"),
            "orange",
        ),
        (["debit", "3150", "-d", "apple"], "debit", Decimal("3150.00"), "apple"),
    ],
)
def test_debit_credit(args, command, amount, description):
    assert main.parse_args(args) == argparse.Namespace(
        command=command, amount=amount, description=description
    )


@pytest.mark.parametrize(
    "args, balance", [(["report"], False), (["report", "--balance"], True)]
)
def test_report(args, balance):
    assert main.parse_args(args) == argparse.Namespace(command="report", balance=balance)


@pytest.mark.parametrize("args", [["date", "01/01/1970"], ["date", "--advance", "0.5"]])
def test_bad_arguments(args):
    with pytest.raises(argparse.ArgumentError):
        main.parse_args(args)