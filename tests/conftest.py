from gltest.direct import sdk_loader

sdk_loader.get_latest_version = lambda: "v0.2.12"

# The pinned Windows gltest loader keeps stdin open on its temporary file and
# then immediately unlinks it.  Windows rejects that unlink even though the
# Direct Mode contract execution itself is valid.  Keep the file alive for the
# test process; this is test-tooling compatibility only and does not affect
# deployable contract sources.
def pytest_configure(config):
    import os
    import tempfile
    from gltest.direct import loader

    def inject(vm):
        from genlayer.py import calldata
        from genlayer.py.types import Address
        sender = vm.sender if isinstance(vm.sender, Address) else Address(vm.sender)
        contract = vm._contract_address if isinstance(vm._contract_address, Address) else Address(vm._contract_address)
        origin = vm.origin if isinstance(vm.origin, Address) else (Address(vm.origin) if vm.origin else None)
        encoded = calldata.encode({"contract_address": contract, "sender_address": sender, "origin_address": origin, "stack": [], "value": vm._value, "datetime": vm._datetime, "is_init": False, "chain_id": vm._chain_id, "entry_kind": 0, "entry_data": b"", "entry_stage_data": None})
        fd, path = tempfile.mkstemp()
        os.write(fd, encoded)
        os.lseek(fd, 0, os.SEEK_SET)
        vm._original_stdin_fd = os.dup(0)
        os.dup2(fd, 0)
        os.close(fd)
        vm._custodia_test_stdin = path

    loader._inject_message_to_fd0 = inject
