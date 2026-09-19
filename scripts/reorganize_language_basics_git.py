# scripts/reorganize_language_basics_git.py
import subprocess
import os

BASE_DIR = r"D:\Projects\knowledgebase"

def run_git(cmd):
    print(f"Running: {cmd}")
    res = subprocess.run(cmd, cwd=BASE_DIR, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error: {res.stderr}")
    else:
        print(f"Success: {res.stdout.strip()}")

# 1. Python FastAPI renames (01-05 to 08-12)
py_renames = [
    ("08-backend-python-fastapi/05_high_performance_asgi_starlette_uvicorn.md", "08-backend-python-fastapi/12_high_performance_asgi_starlette_uvicorn.md"),
    ("08-backend-python-fastapi/04_background_tasks_and_celery.md", "08-backend-python-fastapi/11_background_tasks_and_celery.md"),
    ("08-backend-python-fastapi/03_dependency_injection_system.md", "08-backend-python-fastapi/10_dependency_injection_system.md"),
    ("08-backend-python-fastapi/02_pydantic_v2_validation_and_serialization.md", "08-backend-python-fastapi/09_pydantic_v2_validation_and_serialization.md"),
    ("08-backend-python-fastapi/01_asyncio_event_loop_and_concurrency.md", "08-backend-python-fastapi/08_asyncio_event_loop_and_concurrency.md"),
]
for src, dst in py_renames:
    run_git(f'git mv "{src}" "{dst}"')

# 2. Java renames (existing files 01-06 to 08-13)
java_renames = [
    ("09-backend-java-springboot/06_concurrenthashmap_and_thread_safe_collections.md", "09-backend-java-springboot/08_concurrenthashmap_and_thread_safe_collections.md"),
    ("09-backend-java-springboot/05_jvm_garbage_collectors_zgc_g1_tuning.md", "09-backend-java-springboot/09_jvm_garbage_collectors_zgc_g1_tuning.md"),
    ("09-backend-java-springboot/04_java21_virtual_threads_and_structured_concurrency.md", "09-backend-java-springboot/10_java21_virtual_threads_and_structured_concurrency.md"),
    ("09-backend-java-springboot/03_springboot_microservices_and_resilience4j.md", "09-backend-java-springboot/13_springboot_microservices_and_resilience4j.md"),
    ("09-backend-java-springboot/02_springboot_security_jwt_oauth2.md", "09-backend-java-springboot/12_springboot_security_jwt_oauth2.md"),
    ("09-backend-java-springboot/01_springboot_architecture_and_jvm.md", "09-backend-java-springboot/11_springboot_architecture_and_jvm.md"),
]
for src, dst in java_renames:
    run_git(f'git mv "{src}" "{dst}"')

# 3. JavaScript cleanup of legacy duplicates
js_removals = [
    "02-javascript/01_v8_event_loop_and_microtasks.md",
    "02-javascript/02_closures_lexical_scope_memory.md",
    "02-javascript/03_prototypes_and_prototypal_inheritance.md",
    "02-javascript/04_this_keyword_call_apply_bind.md"
]
for item in js_removals:
    if os.path.exists(os.path.join(BASE_DIR, item)):
        run_git(f'git rm "{item}"')

# 4. JavaScript renames to clean 01-18 sequential order
# First, rename high numbers descending to avoid collision
js_renames = [
    ("02-javascript/15_dom_events_delegation_bubbling.md", "02-javascript/18_dom_events_delegation_bubbling.md"),
    ("02-javascript/14_proxy_and_reflect_api.md", "02-javascript/17_proxy_and_reflect_api.md"),
    ("02-javascript/13_modules_cjs_vs_esm.md", "02-javascript/16_modules_cjs_vs_esm.md"),
    ("02-javascript/12_async_await_generators_iterators.md", "02-javascript/15_async_await_generators_iterators.md"),
    ("02-javascript/11_promises_deep_dive.md", "02-javascript/14_promises_deep_dive.md"),
    ("02-javascript/10_event_loop_microtasks_macrotasks.md", "02-javascript/13_event_loop_microtasks_macrotasks.md"),
    ("02-javascript/06_v8_memory_garbage_collection.md", "02-javascript/12_v8_memory_garbage_collection.md"),
    ("02-javascript/09_es6_classes_under_the_hood.md", "02-javascript/11_es6_classes_under_the_hood.md"),
    ("02-javascript/08_prototypes_and_inheritance.md", "02-javascript/10_prototypes_and_inheritance.md"),
    ("02-javascript/07_this_keyword_and_binding.md", "02-javascript/09_this_keyword_and_binding.md"),
    ("02-javascript/05_closures_and_lexical_scope.md", "02-javascript/08_closures_and_lexical_scope.md"),
    ("02-javascript/04_execution_context_call_stack.md", "02-javascript/07_execution_context_call_stack.md"),
    ("02-javascript/03_functions_first_class_higher_order.md", "02-javascript/06_functions_first_class_higher_order.md"),
    # newly generated files (not yet tracked in git, so normal rename or git mv if staged)
]
for src, dst in js_renames:
    run_git(f'git mv "{src}" "{dst}"')

# Rename the newly generated files if needed
new_js_renames = [
    ("02-javascript/04_objects_destructuring_rest_spread_and_cloning.md", "02-javascript/05_objects_destructuring_rest_spread_and_cloning.md"),
    ("02-javascript/03_arrays_in_depth_methods_and_iteration.md", "02-javascript/04_arrays_in_depth_methods_and_iteration.md"),
    ("02-javascript/02_operators_control_flow_and_loops.md", "02-javascript/03_operators_control_flow_and_loops.md"),
]
for src, dst in new_js_renames:
    s = os.path.join(BASE_DIR, src)
    d = os.path.join(BASE_DIR, dst)
    if os.path.exists(s):
        os.rename(s, d)
        print(f"Renamed {s} -> {d}")

print("Done reorganization!")
