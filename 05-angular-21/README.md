# 🅰️ 05 - Modern Angular 21 Architecture

> Production-grade guide to modern Angular 21: Zoneless change detection, fine-grained Signals reactivity, `@defer` template chunking, Built-in Control Flow (`@if`, `@for`), Signal Inputs/Outputs/Model, Functional Routing, Standalone components, and the `inject()` API.

---

## 🗂️ Module Contents & Learning Path

* [**`01_angular21_signals_and_reactivity.md`**](./01_angular21_signals_and_reactivity.md)
  - `signal()`, `computed()`, `effect()`, signal inputs (`input()`), and two-way `model()` binding.
* [**`02_angular21_zoneless_architecture.md`**](./02_angular21_zoneless_architecture.md)
  - Default zoneless change detection in Angular 21, removal of `zone.js`, and signal dirty marking.
* [**`03_angular21_defer_block_and_lazy_loading.md`**](./03_angular21_defer_block_and_lazy_loading.md)
  - Template-level lazy loading via `@defer`, `@placeholder`, `@loading`, and `@error` triggers (`on viewport`, `on interaction`, `when condition`).
* [**`04_angular21_standalone_components_and_inject.md`**](./04_angular21_standalone_components_and_inject.md)
  - Standalone component architecture, the functional `inject()` API, and environment providers.
* [**`05_angular21_rxjs_interop_to_signal.md`**](./05_angular21_rxjs_interop_to_signal.md)
  - Bridging asynchronous RxJS streams with synchronous Signals via `toSignal()` and `toObservable()`.
* [**`06_angular21_built_in_control_flow_and_optimization.md`**](./06_angular21_built_in_control_flow_and_optimization.md)
  - Modern Built-in Control Flow (`@if`, `@else`, `@for` with mandatory `track`, `@empty`, `@switch`), compiler code generation, and 90% diffing speedup over legacy `*ngFor`.
* [**`07_angular21_signal_inputs_outputs_model_and_queries.md`**](./07_angular21_signal_inputs_outputs_model_and_queries.md)
  - Signal Inputs (`input.required()`), Signal Outputs (`output()`), Two-Way Data Binding with `model()`, and Signal Queries (`viewChild()`).
* [**`08_angular21_modern_routing_functional_guards_and_interceptors.md`**](./08_angular21_modern_routing_functional_guards_and_interceptors.md)
  - Functional Route Guards (`canActivate: [() => inject(...)]`), `RedirectCommand`, `withComponentInputBinding()`, and functional HTTP interceptors (`withInterceptors`).
* [**`interview-questions/README.md`**](./interview-questions/README.md)
  - 📖 **Angular 21 Master Interview Directory (50 Deep Dive Questions)**:
    - ⚡ [Part 1: Signals, Zoneless & Modern Reactivity (Q1 - Q25)](./interview-questions/01_angular_signals_zoneless_and_reactivity_qna.md)
    - 🏛️ [Part 2: Architecture, SSR, Routing & Performance (Q26 - Q50)](./interview-questions/02_angular_di_routing_ssr_and_performance_qna.md)
* [**`interview-questions/angular21_top_interview_questions.md`**](./interview-questions/angular21_top_interview_questions.md)
  - High-frequency Angular 21 senior technical interview questions and architectural answers.

