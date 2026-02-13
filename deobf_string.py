# Tool Decode String (PRENIUM)
# COPYRIGHT: MinhNguyen2412
イント = False
def signal_handler(シ, フ):
    global イント
    if not イント:
        メ = Text("\n\nCtrl+C detected! Stopping immediately...", style="bold yellow")
        プ = "\n\nCtrl+C detected! Stopping immediately..."
        try:
            if リッチ:
                コン.print(Panel(メ, border_style="yellow", expand=False))
            else:print(プ, flush=True)
        except Exception:print(プ, flush=True)
        イント = True
__import__('signal').signal(__import__('signal').SIGINT, signal_handler)
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
    from rich.panel import Panel
    from rich.text import Text
    コン = Console()
    リッチ = True
except ImportError:
    print("Warning: 'rich' library not found. Falling back to basic console output.")
    print("Install 'rich' for enhanced visuals: pip install rich")
    リッチ = False
    class Progress:
        def __init__(セ, *ア, **カ): pass
        def __enter__(セ): return セ
        def __exit__(セ, エ, バ, ト): pass
        def add_task(セ, デ, ト): return 0
        def update(セ, タ, *, アド=None, デ=None, **フ): pass
    class BarColumn: pass
    class TextColumn: pass
    class TimeElapsedColumn: pass
    class SpinnerColumn: pass
    class DummyConsole:
        def print(セ, *ア, **カ):
            プ = [__import__('re').sub(r'\[/?(bold|green|yellow|red|cyan)\]', '', str(ア)) for ア in ア]
            print(*プ)
    コン = DummyConsole()
try:アン = getattr(__import__('ast'), 'unparse')
except AttributeError:
    try:
        アン = getattr(__import__('astor'), 'to_source')
        if リッチ:コン.print(Panel(Text("Using 'astor' for unparsing.", style="italic cyan"), border_style="cyan", expand=False))
        else:print("Using 'astor' for unparsing.")
    except ImportError:
        エ = Text("This script requires Python 3.9+ or the 'astor' library.\nPlease install 'astor': pip install astor", style="bold red")
        if リッチ:コン.print(Panel(エ, border_style="red", title="Error", expand=False))
        else:
            print("Error: This script requires Python 3.9+ or the 'astor' library.")
            print("Please install 'astor': pip install astor")
        __import__('sys').exit(1)

class SkipStatementException(Exception):pass
class DEOBF_STRING(object):
    def __init__(セ):
        セ.デコ = {}
        セ.エバ = {}
        セ.パ = None
        セ.ア = None
        セ.ロ = None
        セ.オ = None
        セ.ラ = -1
        セ.ビ = []
        セ.フ = {}
        for キ, バ in __import__('builtins').__dict__.items():
            if isinstance(バ, type) and issubclass(バ, BaseException):セ.ビ.append(キ)
            if callable(__import__('builtins').__dict__[キ]):セ.フ[キ] = eval(キ)
        ト = None
        while True:
            セ.clear_()
            try:
                コ = '#'*42
                print(コ)
                フ = [フ_ナ for フ_ナ in __import__('os').listdir(__import__('os').getcwd()) if フ_ナ.endswith((".pyc", ".py", ".txt", ".exe"))]
                for イ, フ_ナ in enumerate(フ, start=1):
                    print("[ " + フ_ナ + " ]", end=" ")
                    if イ % 3 == 0:print()
                print()
                print(コ)
                セ.パ = コン.input("[bold green]Enter input file path: [/]")
                if not __import__('os').path.exists(セ.パ):raise FileNotFoundError(f"Input file not found at '{セ.パ}'")
                ディ = __import__('os').path.dirname(セ.パ) or '.'
                ベ = __import__('os').path.basename(セ.パ)
                ナ, エ = __import__('os').path.splitext(ベ)
                セ.ア = __import__('os').path.join(ディ, f'{ナ}_deobf{エ}')
                セ.ロ = __import__('os').path.join(ディ, f'{ナ}_records.json')
                if リッチ:
                    コン.print(Panel(
                        Text.assemble(
                            ("Input file: ", "bold cyan"), (セ.パ, "white"), ("\nOutput file: ", "bold cyan"), (セ.ア, "white"),
                            ("\nRecords file: ", "bold cyan"), (セ.ロ, "white")
                        ),
                        border_style="green",
                        title="File Configuration",
                        expand=False
                    ))
                else:
                    コン.print(f'Input file: {セ.パ}')
                    コン.print(f'Output file: {セ.ア}')
                    コン.print(f'Records file: {セ.ロ}')
                コン.print(Text("Cleaning source code...", style="italic cyan"))
                ソ = セ.CLEAN_CODE(open(セ.パ, 'r', encoding='utf-8').read())
                コン.print(Text('\nAnalyzing and cleaning setup code...', style="italic cyan"))
                if リッチ:
                    プ = Progress(
                        SpinnerColumn(),
                        TextColumn('[progress.description]{task.description}'),
                        BarColumn(),
                        TextColumn('[progress.percentage]{task.percentage:>3.0f}%'),
                        TimeElapsedColumn(),
                        console=コン,
                        transient=False,
                    )
                    プ.start()
                    タ_イ = プ.add_task('[cyan]Identifying Decoders...', total=1)
                    タ_ト = プ.add_task('[cyan]Transforming ast...', total=1)
                else:プ = None
                try:セッ = セ.filter_code(ソ)
                except SyntaxError as エ:
                    if リッチ:
                        コン.input(Panel(
                            Text(f"Invalid Python syntax in input file '{セ.パ}' during initial parse.\nError details: {エ}", style="bold red"),
                            border_style="red", title="Syntax Error", expand=False
                        ))
                    else:
                        コン.print(f"[bold red]ERROR: Invalid Python syntax in input file '{セ.パ}' during initial parse.[/]")
                        コン.input(f'[bold red]Error details: {エ}[/]')
                    continue
                except Exception as エ:
                    if リッチ:
                        コン.input(Panel(
                            Text(f"ERROR during setup code cleaning: {エ}", style="bold red"),
                            border_style="red", title="Processing Error", expand=False
                        ))
                        __import__('traceback').print_exc()
                    else:
                        コン.input(f'[bold red]ERROR during setup code cleaning: {エ}[/]')
                        __import__('traceback').print_exc()
                    continue
                イ_グ = {カ: globals()[カ] for カ in globals().keys() if not カ.startswith('__')}
                try:
                    if セッ:
                        コン.print(Text('Executing process to identify decoder functions...', style="italic cyan"))
                        exec(f"""
_オリ: __import__('typing').Dict[__import__('typing').Tuple[__import__('typing').Union[__import__('types').ModuleType, object], str], __import__('typing').Callable] = {{}}
def _resolve_target(リ, ナ) -> __import__('typing').Tuple[object, str]:
    パ = ナ.split('.')
    パレ = リ
    for パー in パ[:-1]:パレ = getattr(パレ, パー)
    return パレ, パ[-1]
def bypass_library_functions(マ, バイ: __import__('typing').Callable = lambda *ア, **カ: None) -> None:
    for リ_ナ, フ_ナ in マ.items():
        try:リ = __import__('importlib').import_module(リ_ナ)
        except ModuleNotFoundError:continue
        for フ_ナ_イ in フ_ナ:
            try:
                パレ, アト = _resolve_target(リ, フ_ナ_イ)
                if (パレ, アト) not in _オリ:
                    オ = getattr(パレ, アト)
                    _オリ[(パレ, アト)] = オ
                    setattr(パレ, アト, バイ)
            except AttributeError:continue
def restore_imports() -> None:
    for (パレ, アト), オ in list(_オリ.items()):
        setattr(パレ, アト, オ)
        _オリ.pop((パレ, アト), None)
リ_バ = {{
    'telebot': ['TeleBot'],
    'os': ['remove', 'system', 'unlink', 'makedirs', 'rename', 'replace', 'rmdir', 'removedirs'],
    'shutil': ['rmtree', 'copy', 'copy2', 'copyfile', 'copytree', 'move'],
    'builtins': ['exit', 'quit', 'exec', 'print'],
    'sys': ['exit'],
    'pathlib': ['Path.rename', 'Path.unlink', 'Path.rmdir', 'Path.write_text', 'Path.write_bytes']
}}
bypass_library_functions(リ_バ)
{セッ}
restore_imports()
""", globals())
                        コン.print(Text('Setup code executed. Identifying decoders...', style="italic green"))
                    else:
                        if リッチ:
                            コン.print(Panel(
                                Text("Setup code appears empty after cleaning. No decoders might be found.", style="bold yellow"),
                                border_style="yellow", title="Warning", expand=False
                            ))
                        else:コン.print('[yellow]Warning: Setup code appears empty after cleaning. No decoders might be found.[/]')
                except Exception as エ:
                    if リッチ:
                        コン.print(Panel(
                            Text(f"ERROR executing cleaned setup code: {エ}", style="bold red"),
                            border_style="red", title="Execution Error", expand=False
                        ))
                        __import__('traceback').print_exc()
                    else:
                        コン.print(f'\n[bold red]ERROR executing cleaned setup code: {エ}[/]')
                        __import__('traceback').print_exc()
                except SystemExit:コン.print(Text("Bypassing anti-decoding protections...", style="italic yellow"))
                ニ = セ.collect_top_level_names(セッ)
                コン.print(Text('Analyzing new global definitions...', style="italic cyan"))
                フ_ブ = {}
                for ナ in ニ:
                    try:
                        オ = globals()[ナ]
                        ラ = False
                        if isinstance(オ, (__import__('types').FunctionType, __import__('types').LambdaType)):
                            try:
                                フ_フ = getattr(オ.__code__, 'co_filename', None)
                                if フ_フ and ('<string>' in フ_フ or '<exec>' in フ_フ or not フ_フ.endswith('.py')):ラ = True
                            except Exception:ラ = True
                        if ラ:
                            セ.デコ[ナ] = オ
                            セ.エバ[ナ] = オ
                            if リッチ:コン.print(Text(f"  Detected function: {ナ}", style="green"))
                            else:コン.print(f'  Detected func: {ナ}')
                        elif isinstance(オ, (type, __import__('types').BuiltinFunctionType, __import__('types').BuiltinMethodType)):
                            if ナ in イ_グ and globals()[ナ] is イ_グ.get(ナ):continue
                            セ.エバ[ナ] = オ
                            if リッチ:コン.print(Text(f"  Detected variable: {ナ} = {getattr(オ, '__name__', repr(オ))}", style="cyan"))
                            else:コン.print(f"  Detected vars: {ナ} = {getattr(オ, '__name__', repr(オ))}")
                            if getattr(オ, '__name__', repr(オ)) in セ.フ.keys():
                                フ_ブ[ナ] = getattr(オ, '__name__', repr(オ))
                                セ.デコ[ナ] = getattr(オ, '__name__', repr(オ))
                    except KeyError:continue
                if not セ.デコ:
                    if リッチ:
                        コン.print(Panel(
                            Text("Function not identified, try decoding manually...", style="bold yellow"),
                            border_style="yellow", title="Warning", expand=False
                        ))
                    else:コン.print('[bold yellow]Warning: Function not identified, try decoding manually...[/]')
                コン.print(Text('Updating __builtins__ functions...', style="italic cyan"))
                for ナ, デ_オ in {**{'True': True, 'False': False, 'None': None}, **セ.フ}.items():
                    if ナ not in セ.エバ:セ.エバ[ナ] = デ_オ
                if プ:プ.update(タ_イ, advance=1)
                コン.print(Text(f'\nParsing original AST for decoding: {セ.パ}...', style="italic cyan"))
                try:
                    ト = __import__('ast').parse(ソ)
                    コン.print(Text("Restoring variable values to original positions...", style="italic green"))
                    for ボ in __import__('ast').walk(ト):
                        if isinstance(ボ, __import__('ast').Call):
                            if isinstance(ボ.func, __import__('ast').Name):
                                if ボ.func.id in フ_ブ.keys():ボ.func.id = フ_ブ[ボ.func.id]
                        if isinstance(ボ, __import__('ast').Assign):
                            if isinstance(ボ.value, __import__('ast').Name):
                                if ボ.value.id in フ_ブ.keys():ボ.value.id = フ_ブ[ボ.value.id]
                except SyntaxError as エ:
                    if リッチ:
                        コン.input(Panel(
                            Text(f"Invalid Python syntax in input file '{セ.パ}' during second parse.\nError details: {エ}", style="bold red"),
                            border_style="red", title="Syntax Error", expand=False
                        ))
                    else:
                        コン.print(f"[bold red]ERROR: Invalid Python syntax in input file '{セ.パ}' during second parse.[/]")
                        コン.input(f'[bold red]Error details: {エ}[/]')
                    continue
                ト_ス = len(ト.body)
                if プ:プ.update(タ_ト, total=ト_ス)
                ス_デ = DEOBF_STRING.DECODE_STRING(set(セ.デコ.keys()), セ.エバ)
                ス_デ.source = ソ
                コン.print(Text(f'\nStarting transformation...: {セ.ア}', style="italic cyan"))
                ス_プ = 0
                フ_ス = 0
                セ.オ = open(セ.ア, 'w', encoding='utf-8')
                for イ, ス in enumerate(ト.body):
                    if イント:
                        if リッチ:
                            コン.print(Panel(
                                Text("Interruption detected, stopping transformation loop.", style="bold yellow"),
                                border_style="yellow", title="Interrupted", expand=False
                            ))
                        else:コン.print('\n[yellow]Interruption detected, stopping transformation loop.[/]')
                        break
                    セ.ラ = イ
                    カ_ス = イ + 1
                    カ_リ = getattr(ス, 'lineno', '?')
                    if プ:
                        デ = f'[cyan]Line ~{カ_リ} | Attempts: {ス_デ.overall_attempt_count}'
                        プ.update(タ_ト, description=デ, advance=1)
                    else:
                        if (イ + 1) % 20 == 0:コン.print(f'  Processed {イ + 1}/{ト_ス}...')
                    try:
                        ト_ス_イ = ス_デ.visit(ス)
                        if イント:
                            if リッチ:
                                コン.print(Panel(
                                    Text(f"Interrupted during visit of statement {カ_ス}, stopping.", style="bold yellow"),
                                    border_style="yellow", title="Interrupted", expand=False
                                ))
                            else:コン.print(f'\n[yellow]Interrupted during visit of statement {カ_ス}, stopping.[/]')
                            break
                        if ト_ス_イ is None:pass
                        elif isinstance(ト_ス_イ, list):
                            for ス_モ in ト_ス_イ:
                                __import__('ast').fix_missing_locations(ス_モ)
                                セ.オ.write(アン(ス_モ))
                                セ.オ.write('\n')
                        else:
                            __import__('ast').fix_missing_locations(ト_ス_イ)
                            セ.オ.write(アン(ト_ス_イ))
                            セ.オ.write('\n')
                        ス_プ += 1
                    except SkipStatementException as ス_エ:
                        フ_ス += 1
                        エ_メ = Text(f"Skipping statement {カ_ス} (Line ~{カ_リ}) due to decode failure: {ス_エ}", style="bold yellow")
                        if リッチ:コン.print(Panel(エ_メ, border_style="yellow", title="Skipped Statement", expand=False))
                        else:
                            コン.print(f'\n[bold yellow]Skipping statement {カ_ス} (Line ~{カ_リ}) due to decode failure: {ス_エ}[/]')
                        セ.オ.write(f'\n# --- Statement at line ~{カ_リ} skipped due to internal decoding failure: {ス_エ} ---\n\n')
                        continue
                    except Exception as エ:
                        フ_ス += 1
                        エ_メ = Text(f"ERROR processing statement {カ_ス} (Line ~{カ_リ}): {エ}", style="bold red")
                        if リッチ:
                            コン.print(Panel(エ_メ, border_style="red", title="Processing Error", expand=False))
                            コン.print(Text("Attempting to write original statement source due to error...", style="italic yellow"))
                        else:
                            コン.print(f'[bold red]{エ_メ}[/]')
                            コン.print('[yellow]Attempting to write original statement source due to error...[/]')
                        try:
                            オ_ス = __import__('ast').get_source_segment(ソ, ス)
                            if オ_ス:
                                セ.オ.write(f'\n# --- ERROR: Processing failed for the block below (line ~{カ_リ}). Original source: ---')
                                セ.オ.write('\n')
                                セ.オ.write(オ_ス)
                                セ.オ.write('\n# --- END OF FAILED BLOCK ---\n\n')
                            else:
                                セ.オ.write(f'\n# ERROR: Processing failed for statement at line {カ_リ} AND could not retrieve original source.\n\n')
                            ス_プ += 1
                        except Exception as ネ_エ:
                            ファ_メ = Text(f"FATAL: Could not write original source for statement {カ_ス} after error: {ネ_エ}", style="bold red")
                            if リッチ:コン.print(Panel(ファ_メ, border_style="red", title="Fatal Error", expand=False))
                            else:コン.print(f'[bold red]{ファ_メ}[/]')
                            セ.オ.write(f'\n# FATAL ERROR: Could not process OR write original source for statement near line {カ_リ} . Code may be missing.\n\n')
                if イント and ト:
                    レ_ス = セ.ラ + 1
                    if レ_ス < ト_ス:
                        if リッチ:
                            コン.print(Panel(
                                Text(f"Appending {ト_ス - レ_ス} remaining unprocessed original statements...", style="bold yellow"),
                                border_style="yellow", title="Appending Original Code", expand=False
                            ))
                        else:コン.print(f'\n[yellow]Appending {ト_ス - レ_ス} remaining unprocessed original statements...[/]')
                        ラ_リ = getattr(ト.body[セ.ラ], 'lineno', '?') if セ.ラ >= 0 else '?'
                        セ.オ.write(f'\n\n# --- PROCESSING INTERRUPTED BY USER (Ctrl+C) AFTER LINE ~{ラ_リ} ---')
                        セ.オ.write(f'\n# --- Appending original code for the remaining {ト_ス - レ_ス} statements --- \n\n')
                        for ジョ in range(レ_ス, ト_ス):
                            レ_ス_モ = ト.body[ジョ]
                            try:
                                オ_レ_ソ = アン(レ_ス_モ)
                                セ.オ.write(オ_レ_ソ)
                                セ.オ.write('\n')
                            except Exception as ア_エ:
                                レ_リ = getattr(レ_ス_モ, 'lineno', '?')
                                if リッチ:
                                    コン.print(Panel(
                                        Text(f"ERROR: Could not unparse remaining original statement near line {レ_リ}: {ア_エ}", style="bold red"),
                                        border_style="red", title="Unparse Error", expand=False
                                    ))
                                else:コン.print(f'[bold red]ERROR: Could not unparse remaining original statement near line {レ_リ}: {ア_エ}[/]')
                                セ.オ.write(f'\n# --- ERROR: Could not unparse remaining original statement near line {レ_リ}: {ア_エ} ---\n\n')
                    else:
                        if リッチ:
                            コン.print(Panel(
                                Text("Interruption occurred, but all statements were already processed or attempted.", style="bold yellow"),
                                border_style="yellow", title="Status", expand=False
                            ))
                        else:コン.print('\n[yellow]Interruption occurred, but all statements were already processed or attempted.[/]')
                コン.print(Text('\nFinished processing loop.', style="italic green"))
                コン.print(Text(f'  Statements processed/attempted: {ス_プ}/{ト_ス if ト else "N/A"}', style="cyan"))
                if フ_ス > 0:
                    if リッチ:
                        コン.print(Panel(
                            Text(f"Statements failed transformation (original source written): {フ_ス}", style="bold yellow"),
                            border_style="yellow", title="Warning", expand=False
                        ))
                    else:コン.print(f'  [bold yellow]Statements failed transformation (original source written): {フ_ス}[/]')
                if イント:
                    if プ:プ.stop()
                    if リッチ:
                        コン.print(Panel(
                            Text("Processing was interrupted by user.", style="bold yellow"),
                            border_style="yellow", title="Interrupted", expand=False
                        ))
                    else:コン.print(f'  [bold yellow]Processing was interrupted by user.[/]')
                break
            except FileNotFoundError as エ:
                if リッチ:
                    コン.print(Panel(Text(f"Error: {エ}", style="bold red"), border_style="red", title="File Error", expand=False))
                    コン.input("Press Enter to try again...")
                else:コン.input(f'[bold red]Error: {エ}[/]')
                continue
            except SyntaxError as エ:
                if プ:プ.stop()
                if リッチ:
                    コン.print(Panel(
                        Text(f"Error parsing Python code in '{セ.パ}': {エ}\nPlease check the Python syntax of the input file.", style="bold red"),
                        border_style="red", title="Syntax Error", expand=False
                    ))
                    コン.input("Press Enter to try again...")
                else:
                    コン.print(f"[bold red]Error parsing Python code in '{セ.パ}': {エ}[/]")
                    コン.input('[bold red]Please check the Python syntax of the input file.[/]')
                continue
            except IOError as エ:
                タ_フ = セ.ア if セ.オ else セ.パ if セ.パ else 'Unknown File'
                if リッチ:
                    if プ:プ.stop()
                    コン.print(Panel(
                        Text(f"Error performing file I/O on '{タ_フ}': {エ}", style="bold red"),
                        border_style="red", title="IO Error", expand=False
                    ))
                    コン.input("Press Enter to try again...")
                else:コン.input(f"[bold red]Error performing file I/O on '{タ_フ}': {エ}[/]")
                continue
            except (KeyboardInterrupt, EOFError):
                if リッチ:
                    コン.print(Panel(
                        Text("KeyboardInterrupt caught directly. Exiting potentially uncleanly.", style="bold red"),
                        border_style="red", title="Fatal Interrupt", expand=False
                    ))
                else:コン.print('\n[bold red]KeyboardInterrupt caught directly. Exiting potentially uncleanly.[/]')
                __import__('sys').exit(1)
            except Exception as エ:
                if リッチ:
                    コン.print(Panel(
                        Text("An unexpected error occurred during processing:", style="bold red"),
                        border_style="red", title="Unexpected Error", expand=False
                    ))
                    __import__('traceback').print_exc()
                else:
                    コン.print(f'\n[bold red]An unexpected error occurred during processing:[/]')
                    __import__('traceback').print_exc()
                __import__('sys').exit(1)
            finally:
                if セ.オ:
                    try:セ.オ.close()
                    except IOError as エ:
                        if リッチ:
                            コン.print(Panel(
                                Text(f"Error closing output file '{セ.ア}': {エ}", style="bold red"),
                                border_style="red", title="File Close Error", expand=False
                            ))
                        else:
                            コン.print(f"[bold red]Error closing output file '{セ.ア}': {エ}[/]")          
        if プ:プ.stop()
        while True:
            チ_バ = str(コン.input('[bold green]Change code location optimization (y/n): [/]'))
            if チ_バ.upper() == 'Y':
                コン.print(Text("Restoring variable positions...", style="italic cyan"))
                コ = アン(セ.UPDATE_VAR_POSITIONS(__import__('ast').parse(open(セ.ア, 'r', encoding='utf-8').read())))
                open(セ.ア, 'w', encoding='utf-8').write(コ)
                break
            elif チ_バ.upper() == 'N':break
            else:continue
        if 'ス_デ' in locals() and (not イント or ス_プ > 0):
            try:
                コン.print(Text(f'\nWriting decoding records to: {セ.ロ}', style="italic cyan"))
                __import__('json').dump(ス_デ.records, open(セ.ロ, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
            except IOError as エ:
                if リッチ:
                    コン.print(Panel(
                        Text(f"Error writing decoding records to '{セ.ロ}': {エ}", style="bold red"),
                        border_style="red", title="IO Error", expand=False
                    ))
                else:コン.print(f"[bold red]Error writing decoding records to '{セ.ロ}': {エ}[/]")
            except Exception as エ:
                if リッチ:
                    コン.print(Panel(
                        Text(f"Error saving records: {エ}", style="bold red"),
                        border_style="red", title="Record Save Error", expand=False
                    ))
                else:コン.print(f'[bold red]Error saving records: {エ}[/]')
        elif イント and ス_プ == 0:
            if リッチ:
                コン.print(Panel(
                    Text("Skipping saving decoding records due to early interruption.", style="bold yellow"),
                    border_style="yellow", title="Skipped Records", expand=False
                ))
            else:コン.print('\n[yellow]Skipping saving decoding records due to early interruption.[/]')
        if リッチ:
            サ = Text.assemble(
                ("--- Deobfuscation Summary ---\n", "bold cyan"),
                ("  Output code: ", "cyan"), (f"{セ.ア}\n", "white" if __import__('os').path.exists(セ.ア) else "yellow"),
                ("  Records log: ", "cyan"), (f"{セ.ロ}\n" if __import__('os').path.exists(セ.ロ) else f"{セ.ロ} (File may not exist or failed to write)\n", "white" if __import__('os').path.exists(セ.ロ) else "yellow"),
                ("  Total successful decodes: ", "cyan"), (f"{ス_デ.overall_success_count}\n", "white"),
                ("  Total decode attempts: ", "cyan"), (f"{ス_デ.overall_attempt_count}\n", "white")
            )
            if フ_ス > 0:サ.append(Text(f"  Note: {フ_ス} statements could not be processed and were written in original form.\n", style="bold yellow"))
            if イント:サ.append(Text(f"  Note: Process was interrupted by user. Remaining original code (if any) appended to output file.\n", style="bold yellow"))
            サ.append(Text("--- End Summary ---", style="bold cyan"))
            コン.print(Panel(サ, border_style="cyan", title="Summary", expand=False))
        else:
            コン.print(f'\n--- Deobfuscation Summary ---')
            コン.print(f'  Output code: {セ.ア}' if __import__('os').path.exists(セ.ア) else f'  Output code: {セ.ア} (File may not exist or be incomplete)')
            if セ.ロ:コン.print(f'  Records log: {セ.ロ}' if __import__('os').path.exists(セ.ロ) else f'  Records log: {セ.ロ} (File may not exist or failed to write)')
            コン.print(f'  Total successful decodes: {ス_デ.overall_success_count}')
            コン.print(f'  Total decode attempts: {ス_デ.overall_attempt_count}')
            if フ_ス > 0:コン.print(f'  [bold yellow]Note: {フ_ス} statements could not be processed and were written in original form.[/]')
            if イント:コン.print(f'  [bold yellow]Note: Process was interrupted by user. Remaining original code (if any) appended to output file.[/]')
            コン.print(f'--- End Summary ---')
    def clear_(セ):__import__('os').system("cls" if __import__('os').name == "nt" else "clear")
    def CLEAN_CODE(セ, ダ):
        ト = __import__('ast').parse(ダ)
        ト_ノ = sum(1 for _ in __import__('ast').walk(ト))
        with Progress() as プ:
            タ_イ = プ.add_task('[cyan]Cleaning Code...', total=ト_ノ)
            class CLEAN_UP(__import__('ast').NodeTransformer):
                def __init__(セ, ソ, プ, タ):
                    セ.ソ = ソ
                    セ.プ = プ
                    セ.タ = タ
                def visit_Module(セ, ノ):
                    ノ.body = [
                        n for n in ノ.body if not (
                            isinstance(n, __import__('ast').Expr) and 
                            isinstance(n.value, __import__('ast').Constant) and 
                            isinstance(n.value.value, str)
                        )
                    ]
                    return セ.generic_visit(ノ)
                def visit_FunctionDef(セ, ノ):
                    ノ.body = [
                        n for n in ノ.body if not (
                            isinstance(n, __import__('ast').Expr) and 
                            isinstance(n.value, __import__('ast').Constant) and 
                            isinstance(n.value.value, str)
                        )
                    ]
                    return セ.generic_visit(ノ)
                def generic_visit(セ, ノ):
                    セ.プ.advance(セ.タ)
                    if hasattr(ノ, 'body') and isinstance(ノ.body, list):
                        ノ.body = [
                            n for n in ノ.body if not (
                                isinstance(n, __import__('ast').Expr) and 
                                isinstance(n.value, __import__('ast').Constant) and 
                                isinstance(n.value.value, str)
                            )
                        ]
                    if hasattr(ノ, 'orelse') and isinstance(ノ.orelse, list):
                        ノ.orelse = [
                            n for n in ノ.orelse if not (
                                isinstance(n, __import__('ast').Expr) and 
                                isinstance(n.value, __import__('ast').Constant) and 
                                isinstance(n.value.value, str)
                            )
                        ]
                    return super().generic_visit(ノ)
            return アン(CLEAN_UP(ダ, プ, タ_イ).visit(ト))
    class FilterCalls(__import__('ast').NodeTransformer):
        def _get_call_name(セ, フ):
            if isinstance(フ, __import__('ast').Name):return フ.id
            elif isinstance(フ, __import__('ast').Attribute):
                if isinstance(フ.value, __import__('ast').Call):
                    カ_バ = フ.value
                    if (
                        isinstance(カ_バ.func, __import__('ast').Name)
                        and カ_バ.func.id == '__import__'
                        and len(カ_バ.args) == 1
                        and isinstance(カ_バ.args[0], (__import__('ast').Constant, __import__('ast').Name))
                    ):
                        モ_ア = カ_バ.args[0]
                        if isinstance(モ_ア, __import__('ast').Constant):モ_ス = repr(モ_ア.value)
                        else:モ_ス = アン(モ_ア).strip()
                        return f"__import__({モ_ス}).{フ.attr}"
                バ_ナ = セ._get_call_name(フ.value)
                if バ_ナ:return f"{バ_ナ}.{フ.attr}"
                return None
            elif isinstance(フ, __import__('ast').Subscript):
                バ_ナ = セ._get_call_name(フ.value)
                if (バ_ナ
                    and isinstance(フ.slice, __import__('ast').Constant)
                    and isinstance(フ.slice.value, str)):
                    return f"{バ_ナ}.{フ.slice.value}"
                return None
            elif isinstance(フ, __import__('ast').Call):
                if (isinstance(フ.func, __import__('ast').Name)
                    and len(フ.args) >= 2
                    and isinstance(フ.args[1], __import__('ast').Constant)
                    and isinstance(フ.args[1].value, str)):
                    オ_ソ = アン(フ.args[0]).strip()
                    アト = フ.args[1].value
                    return f"{フ.func.id}({オ_ソ}, '{アト}')"
                return None
            elif isinstance(フ, __import__('ast').Lambda):return 'lambda'
            return None
        def visit_FunctionDef(セ, ノ):return ノ
        def visit_ClassDef(セ, ノ):return ノ
        def visit_Assign(セ, ノ):return セ.generic_visit(ノ)
        def visit_Expr(セ, ノ):
            if not isinstance(ノ.value, __import__('ast').Call):return セ.generic_visit(ノ)
            カ_ノ = ノ.value
            カ_ナ = セ._get_call_name(カ_ノ.func)
            if カ_ノ.args:
                イ = カ_ノ.args[0]
                ト_イ = セ.visit(イ)
                return __import__('ast').copy_location(__import__('ast').Expr(value=ト_イ), ノ)
            if カ_ナ:
                return __import__('ast').copy_location(__import__('ast').Expr(value=__import__('ast').Tuple(elts=[], ctx=__import__('ast').Load())), ノ)
            if カ_ノ.args:
                ア = カ_ノ.args[0]
                if isinstance(ア, (__import__('ast').Constant, __import__('ast').Str, __import__('ast').Bytes, __import__('ast').JoinedStr)):
                    ト_ア = セ.visit(ア)
                    return __import__('ast').copy_location(__import__('ast').Expr(value=ト_ア), ノ)
            イ_ラ_カ = isinstance(カ_ノ.func, __import__('ast').Lambda)
            ニ_ノ = セ.generic_visit(ノ)
            if イ_ラ_カ and isinstance(ニ_ノ.value, __import__('ast').Call) and isinstance(ニ_ノ.value.func, __import__('ast').Lambda):
                ラ_ノ = ニ_ノ.value.func
                if isinstance(ラ_ノ.body, __import__('ast').Expr):
                    return __import__('ast').copy_location(__import__('ast').Expr(value=ラ_ノ.body.value), ニ_ノ)
            return ニ_ノ
        def visit_If(セ, ノ):
            ノ.test = セ.visit(ノ.test)
            ニ_ボ, ニ_オ = [], []
            for ス in ノ.body:
                ト_イ = セ.visit(ス)
                if isinstance(ト_イ, list): ニ_ボ.extend(ト_イ)
                elif ト_イ is not None: ニ_ボ.append(ト_イ)
            for ス in ノ.orelse:
                ト_イ = セ.visit(ス)
                if isinstance(ト_イ, list): ニ_オ.extend(ト_イ)
                elif ト_イ is not None: ニ_オ.append(ト_イ)
            ノ.body, ノ.orelse = ニ_ボ, ニ_オ
            if not ノ.body and not ノ.orelse: return None
            if not ノ.body and ノ.orelse: return ニ_オ
            return ノ
    class TopLevelCollector(__import__('ast').NodeVisitor):
        def __init__(セ):
            セ.ナ = set()
            セ.デ = 0
        def visit_FunctionDef(セ, ノ):
            if セ.デ == 0 and ノ.name not in セ.ナ:セ.ナ.add(ノ.name)
            セ.デ += 1
            セ.generic_visit(ノ)
            セ.デ -= 1
        def visit_AsyncFunctionDef(セ, ノ):
            if セ.デ == 0 and ノ.name not in セ.ナ:セ.ナ.add(ノ.name)
            セ.デ += 1
            セ.generic_visit(ノ)
            セ.デ -= 1
        def visit_ClassDef(セ, ノ):
            if セ.デ == 0 and ノ.name not in セ.ナ:セ.ナ.add(ノ.name)
            セ.デ += 1
            セ.generic_visit(ノ)
            セ.デ -= 1
        def visit_Assign(セ, ノ):
            if セ.デ == 0:
                for タ in ノ.targets:
                    if (isinstance(タ, __import__('ast').Subscript) and
                        isinstance(タ.value, __import__('ast').Call) and
                        isinstance(タ.value.func, __import__('ast').Name) and
                        isinstance(タ.slice, __import__('ast').Constant) and
                        isinstance(タ.slice.value, str)):
                        セ.ナ.add(タ.slice.value)
                    else:
                        テ = アン(タ).strip()
                        if テ not in セ.ナ:セ.ナ.add(テ)
            セ.generic_visit(ノ)
    def collect_top_level_names(セ, ソ) -> set:
        コ = DEOBF_STRING.TopLevelCollector()
        コ.visit(__import__('ast').parse(ソ))
        return コ.ナ
    def filter_code(セ, ソ) -> str:
        try:ト = __import__('ast').parse(ソ)
        except SyntaxError as エ:
            if リッチ:
                コン.print(Panel(
                    Text(f"Error parsing source code: {エ}", style="bold red"),
                    border_style="red", title="Parse Error", expand=False
                ))
            else:
                print(f'Error parsing source code: {エ}', file=__import__('sys').stderr)
            return ソ
        ト_フ = DEOBF_STRING.FilterCalls()
        ニ_ト = ト_フ.visit(ト)
        __import__('ast').fix_missing_locations(ニ_ト)
        return アン(ニ_ト)
    def safe_eval_expr(セ, ノ, キ_バ=None) -> __import__('typing').Any:
        if キ_バ is None:キ_バ = {}
        エ_フ = float('nan')
        def _is_eval_fail(バ) -> bool:return isinstance(バ, float) and バ != バ
        def _eval_recursive(ノ, デ) -> __import__('typing').Any:
            if デ > 15:return エ_フ
            if isinstance(ノ, __import__('ast').Constant):
                バ = ノ.value
                if isinstance(バ, (str, bytes, tuple, list, set, dict)):
                    try:
                        if hasattr(バ, '__len__') and (not isinstance(バ, type)):
                            if len(バ) > 100000:return エ_フ
                    except TypeError:pass
                return バ
            elif isinstance(ノ, __import__('ast').Name):return キ_バ.get(ノ.id, エ_フ)
            elif isinstance(ノ, (__import__('ast').Tuple, __import__('ast').List, __import__('ast').Set)):
                エ = []
                if len(ノ.elts) > 100000:return エ_フ
                for エ_イ in ノ.elts:
                    エ_エ = _eval_recursive(エ_イ, デ + 1)
                    if _is_eval_fail(エ_エ):return エ_フ
                    エ.append(エ_エ)
                if isinstance(ノ, __import__('ast').Tuple):return tuple(エ)
                if isinstance(ノ, __import__('ast').List):return list(エ)
                if isinstance(ノ, __import__('ast').Set):
                    try:return set(エ)
                    except TypeError:return エ_フ
            elif isinstance(ノ, __import__('ast').Dict):
                エ_ディ = {}
                if len(ノ.keys) > 100000:return エ_フ
                for キ_ノ, バ_ノ in zip(ノ.keys, ノ.values):
                    if キ_ノ is None:
                        マ_バ = _eval_recursive(バ_ノ, デ + 1)
                        if _is_eval_fail(マ_バ) or not isinstance(マ_バ, dict):return エ_フ
                        if len(エ_ディ) + len(マ_バ) > 100000:return エ_フ
                        try:
                            for ケ in マ_バ.keys():hash(ケ)
                            エ_ディ.update(マ_バ)
                        except TypeError:return エ_フ
                        except Exception:return エ_フ
                        continue
                    ケ = _eval_recursive(キ_ノ, デ + 1)
                    if _is_eval_fail(ケ):return エ_フ
                    try:hash(ケ)
                    except TypeError:return エ_フ
                    バ = _eval_recursive(バ_ノ, デ + 1)
                    if _is_eval_fail(バ):return エ_フ
                    エ_ディ[ケ] = バ
                return エ_ディ
            elif isinstance(ノ, __import__('ast').UnaryOp):
                オ = _eval_recursive(ノ.operand, デ + 1)
                if _is_eval_fail(オ):return エ_フ
                オ_マ = {__import__('ast').UAdd: __import__('operator').pos, __import__('ast').USub: __import__('operator').neg, __import__('ast').Not: __import__('operator').not_, __import__('ast').Invert: __import__('operator').invert}
                オ_ペ = オ_マ.get(type(ノ.op))
                if not オ_ペ:return エ_フ
                try:
                    if isinstance(ノ.op, (__import__('ast').UAdd, __import__('ast').USub, __import__('ast').Invert)):
                        if not isinstance(オ, (int, float, bool, complex)):return エ_フ
                    return オ_ペ(オ)
                except Exception:return エ_フ
            elif isinstance(ノ, __import__('ast').BinOp):
                レ = _eval_recursive(ノ.left, デ + 1)
                if _is_eval_fail(レ):return エ_フ
                リ = _eval_recursive(ノ.right, デ + 1)
                if _is_eval_fail(リ):return エ_フ
                オ_マ = {__import__('ast').Add: __import__('operator').add, __import__('ast').Sub: __import__('operator').sub, __import__('ast').Mult: __import__('operator').mul, __import__('ast').Div: __import__('operator').truediv, __import__('ast').FloorDiv: __import__('operator').floordiv, __import__('ast').Mod: __import__('operator').mod, __import__('ast').Pow: __import__('operator').pow, __import__('ast').LShift: __import__('operator').lshift, __import__('ast').RShift: __import__('operator').rshift, __import__('ast').BitOr: __import__('operator').or_, __import__('ast').BitXor: __import__('operator').xor, __import__('ast').BitAnd: __import__('operator').and_, __import__('ast').MatMult: None}
                オ_ペ = オ_マ.get(type(ノ.op))
                if オ_ペ is None:return エ_フ
                ア = False
                ヌ = (int, float, bool, complex)
                セ = (str, bytes, list, tuple)
                if isinstance(レ, ヌ) and isinstance(リ, ヌ):
                    if isinstance(ノ.op, (__import__('ast').LShift, __import__('ast').RShift, __import__('ast').BitOr, __import__('ast').BitXor, __import__('ast').BitAnd)):ア = isinstance(レ, int) and isinstance(リ, int)
                    else:ア = True
                elif isinstance(ノ.op, __import__('ast').Add) and isinstance(レ, type(リ)) and isinstance(レ, セ):
                    ア = True
                    if len(レ) + len(リ) > 100000:return エ_フ
                elif isinstance(ノ.op, __import__('ast').Mult):
                    if isinstance(レ, int) and isinstance(リ, セ):
                        ア = True
                        if abs(レ) > 10000:return エ_フ
                        if len(リ) * abs(レ) > 100000:return エ_フ
                    elif isinstance(レ, セ) and isinstance(リ, int):
                        ア = True
                        if abs(リ) > 10000:return エ_フ
                        if len(レ) * abs(リ) > 100000:return エ_フ
                if not ア:return エ_フ
                try:
                    if isinstance(ノ.op, __import__('ast').Pow):
                        if isinstance(リ, (int, float)) and abs(リ) > 1000:return エ_フ
                        if isinstance(レ, (int, float, complex)) and レ == 0 and isinstance(リ, (int, float)) and (リ < 0):return エ_フ
                        if isinstance(レ, int) and isinstance(リ, int) and (リ > 0) and (レ != 0):
                            if リ * (レ.bit_length() if レ != 0 else 1) > 1000000:return エ_フ
                    if isinstance(ノ.op, (__import__('ast').Div, __import__('ast').FloorDiv, __import__('ast').Mod)):
                        if isinstance(リ, ヌ) and リ == 0:return エ_フ
                    レ_ス = オ_ペ(レ, リ)
                    if isinstance(レ_ス, (str, bytes, tuple, list, set, dict)):
                        if len(レ_ス) > 100000:return エ_フ
                    if isinstance(レ_ス, float) and (レ_ス != レ_ス or レ_ス == float('inf') or レ_ス == float('-inf')):return エ_フ
                    return レ_ス
                except (ValueError, TypeError, OverflowError, ZeroDivisionError):return エ_フ
                except Exception:return エ_フ
            elif isinstance(ノ, __import__('ast').Compare):
                レ = _eval_recursive(ノ.left, デ + 1)
                if _is_eval_fail(レ):return エ_フ
                オ_マ = {__import__('ast').Eq: __import__('operator').eq, __import__('ast').NotEq: __import__('operator').ne, __import__('ast').Lt: __import__('operator').lt, __import__('ast').LtE: __import__('operator').le, __import__('ast').Gt: __import__('operator').gt, __import__('ast').GtE: __import__('operator').ge, __import__('ast').Is: __import__('operator').is_, __import__('ast').IsNot: __import__('operator').is_not, __import__('ast').In: lambda x, y: x in y, __import__('ast').NotIn: lambda x, y: x not in y}
                オ_バ = True
                カ_レ = レ
                if len(ノ.ops) != len(ノ.comparators):return エ_フ
                for オ_ノ, コ_ノ in zip(ノ.ops, ノ.comparators):
                    オ_ペ = オ_マ.get(type(オ_ノ))
                    if オ_ペ is None:return エ_フ
                    リ = _eval_recursive(コ_ノ, デ + 1)
                    if _is_eval_fail(リ):return エ_フ
                    try:
                        if isinstance(オ_ノ, (__import__('ast').Is, __import__('ast').IsNot)):
                            ア_イ = (type(None), bool)
                            if not (isinstance(カ_レ, ア_イ) and isinstance(リ, ア_イ)):return エ_フ
                        if isinstance(オ_ノ, (__import__('ast').In, __import__('ast').NotIn)):
                            ア_コ = (str, bytes, list, tuple, set, dict)
                            if not isinstance(リ, ア_コ):return エ_フ
                            if isinstance(リ, (set, dict)):hash(カ_レ)
                        コ_レ = オ_ペ(カ_レ, リ)
                        if not isinstance(コ_レ, bool):return エ_フ
                        if not コ_レ:
                            オ_バ = False
                            break
                        カ_レ = リ
                    except TypeError:return エ_フ
                    except Exception:return エ_フ
                return オ_バ
            elif isinstance(ノ, __import__('ast').BoolOp):
                イ_ア = isinstance(ノ.op, __import__('ast').And)
                フ_バ = None
                for イ, バ_ノ in enumerate(ノ.values):
                    バ = _eval_recursive(バ_ノ, デ + 1)
                    if _is_eval_fail(バ):return エ_フ
                    フ_バ = バ
                    イ_ト = bool(バ)
                    if イ_ア and (not イ_ト):return バ
                    if not イ_ア and イ_ト:return バ
                return フ_バ
            elif isinstance(ノ, __import__('ast').Subscript):
                バ = _eval_recursive(ノ.value, デ + 1)
                if _is_eval_fail(バ):return エ_フ
                ア_ベ = (str, bytes, tuple, list, dict)
                if not isinstance(バ, ア_ベ):return エ_フ
                ス = ノ.slice
                try:
                    イ_ノ: __import__('typing').Optional[__import__('ast').expr] = None
                    if isinstance(ス, __import__('ast').Index):イ_ノ = ス.value
                    elif isinstance(ス, __import__('ast').Constant) or isinstance(ス, __import__('ast').Name) or isinstance(ス, __import__('ast').UnaryOp) or isinstance(ス, __import__('ast').BinOp) or isinstance(ス, __import__('ast').IfExp) or isinstance(ス, __import__('ast').Subscript):イ_ノ = ス
                    elif isinstance(ス, __import__('ast').Slice):
                        def eval_slice_part(パ_ノ: __import__('typing').Optional[__import__('ast').expr]) -> __import__('typing').Any:
                            if パ_ノ is None:return None
                            エ_バ = _eval_recursive(パ_ノ, デ + 1)
                            if _is_eval_fail(エ_バ) or (エ_バ is not None and (not isinstance(エ_バ, int))):return エ_フ
                            if isinstance(エ_バ, int) and abs(エ_バ) > __import__('sys').maxsize:return エ_フ
                            return エ_バ
                        ロ = eval_slice_part(ス.lower)
                        ア = eval_slice_part(ス.upper)
                        ステ = eval_slice_part(ス.step)
                        if any((_is_eval_fail(p) for p in (ロ, ア, ステ))):return エ_フ
                        if ステ == 0:return エ_フ
                        if isinstance(バ, (str, bytes, tuple, list)):
                            try:
                                ス_オ = slice(ロ, ア, ステ)
                                イ_ン = ス_オ.indices(len(バ))
                                スタ, スト, エス = イ_ン
                                if エス == 0:ラ_レ = 0
                                elif エス > 0 and スタ >= スト:ラ_レ = 0
                                elif エス < 0 and スタ <= スト:ラ_レ = 0
                                else:
                                    ディ = abs(スト - スタ)
                                    ラ_レ = (ディ + abs(エス) - 1) // abs(エス)
                                if ラ_レ > 100000:return エ_フ
                            except ValueError:return エ_フ
                        return バ[slice(ロ, ア, ステ)]
                    if イ_ノ is not None:
                        イデ = _eval_recursive(イ_ノ, デ + 1)
                        if _is_eval_fail(イデ):return エ_フ
                        if isinstance(バ, (str, bytes, tuple, list)):
                            if not isinstance(イデ, int):return エ_フ
                            if not -len(バ) <= イデ < len(バ):raise IndexError('index out of range')
                        elif isinstance(バ, dict):
                            try:hash(イデ)
                            except TypeError:return エ_フ
                        return バ[イデ]
                    else:return エ_フ
                except (KeyError, IndexError, TypeError, ValueError):return エ_フ
                except Exception:return エ_フ
            elif isinstance(ノ, __import__('ast').IfExp):
                テ_バ = _eval_recursive(ノ.test, デ + 1)
                if _is_eval_fail(テ_バ):return エ_フ
                チュ = ノ.body if テ_バ else ノ.orelse
                return _eval_recursive(チュ, デ + 1)
            elif isinstance(ノ, (__import__('ast').Call, __import__('ast').Attribute, __import__('ast').Lambda, __import__('ast').ListComp, __import__('ast').SetComp, __import__('ast').DictComp, __import__('ast').GeneratorExp, __import__('ast').Await, __import__('ast').Yield, __import__('ast').YieldFrom, __import__('ast').FormattedValue, __import__('ast').JoinedStr, __import__('ast').Starred, __import__('ast').NamedExpr)):return エ_フ
            else:return エ_フ
        try:
            レ_ス = _eval_recursive(ノ, 0)
            return None if _is_eval_fail(レ_ス) else レ_ス
        except RecursionError:return None
        except Exception:return None
    def UPDATE_VAR_POSITIONS(セ, ト: __import__('ast').AST) -> __import__('ast').AST:
        __import__('ast').fix_missing_locations(ト)
        マ_イ = 100
        ト_レ = 0
        プ_コ = None
        タ_イ = None
        if リッチ:
            プ_コ = Progress(SpinnerColumn(), TextColumn('[progress.description]{task.description}'), BarColumn(), TextColumn('[progress.percentage]{task.percentage:>3.0f}%'), TimeRemainingColumn(), TimeElapsedColumn(), console=コン, transient=False)
            タ_イ = プ_コ.add_task('[yellow]Optimizing Consts...', total=マ_イ)
            プ_コ.start()
        try:
            for イ in range(マ_イ):
                if プ_コ and タ_イ is not None:プ_コ.update(タ_イ, description=f'[yellow]Optimizing Consts...')
                ト_ラ = セ.ConstantTransformer(セ)
                ニ_ト = ト_ラ.visit(ト)
                __import__('ast').fix_missing_locations(ニ_ト)
                ト_レ += ト_ラ.replacements_count
                if not ト_ラ.changed:
                    if プ_コ and タ_イ is not None:プ_コ.update(タ_イ, completed=マ_イ, description='[green]Optimization Converged.')
                    コン.print(f'[green]Constant folding converged after {イ + 1} iterations. Total replacements: {ト_レ}')
                    return ニ_ト
                ト = ニ_ト
                if プ_コ and タ_イ is not None:プ_コ.update(タ_イ, advance=1)
            ワ_メ = f'Warning: Optimization did not converge after {マ_イ} iterations. Total replacements: {ト_レ}'
            return ト
        finally:
            if プ_コ:プ_コ.stop()
            if ト_ラ.changed:
                if リッチ:コン.print(Panel(Text(ワ_メ, style='bold green'), border_style='green', title='Optimization Warning', expand=False))
                else:コン.print(ワ_メ, file=__import__('sys').stderr)
    class ConstantTransformer(__import__('ast').NodeTransformer):
        def __init__(セ, オ_セ: 'DEOBF_STRING', イ_バ=None, イ_ア=None):
            super().__init__()
            セ.オ_セ = オ_セ
            セ.バ_バ = イ_バ.copy() if イ_バ is not None else {}
            セ.ア_マ = イ_ア.copy() if イ_ア is not None else {}
            セ.changed = False
            セ.replacements_count = 0
        def _create_constant_node(セ, バ, テ_ノ) -> __import__('ast').Constant:
            try:
                ニ_ノ = __import__('ast').Constant(value=バ)
                __import__('ast').copy_location(ニ_ノ, テ_ノ)
                return ニ_ノ
            except TypeError:return テ_ノ
        def _create_attribute_node(セ, バ: __import__('ast').expr, アト: str, テ_ノ: __import__('ast').AST) -> __import__('ast').Attribute:
            ニ_ノ = __import__('ast').Attribute(value=バ, attr=アト, ctx=__import__('ast').Load())
            __import__('ast').copy_location(ニ_ノ, テ_ノ)
            return ニ_ノ
        def _mark_changed(セ):セ.changed = True
        def _increment_replacement_count(セ):
            セ.replacements_count += 1
            セ.changed = True
        def _update_var(セ, ナ, バ):
            if ナ not in セ.バ_バ or セ.バ_バ[ナ] != バ:
                セ.バ_バ[ナ] = バ
                if ナ in セ.ア_マ:del セ.ア_マ[ナ]
                セ._mark_changed()
        def _update_alias(セ, ナ, ア_ノ):
            カ_ア = セ.ア_マ.get(ナ)
            ニ_ダ = __import__('ast').dump(ア_ノ)
            カ_ダ = __import__('ast').dump(カ_ア) if カ_ア else None
            if ニ_ダ != カ_ダ:
                セ.ア_マ[ナ] = ア_ノ
                if ナ in セ.バ_バ:del セ.バ_バ[ナ]
                セ._mark_changed()
        def _remove_binding(セ, ナ):
            チ_ロ = False
            if ナ in セ.バ_バ:
                del セ.バ_バ[ナ]
                チ_ロ = True
            if ナ in セ.ア_マ:
                del セ.ア_マ[ナ]
                チ_ロ = True
        def _extract_target_names(セ, ノ: __import__('ast').expr) -> __import__('typing').Set[str]:
            ナ = set()
            if isinstance(ノ, __import__('ast').Name):ナ.add(ノ.id)
            elif isinstance(ノ, __import__('ast').Tuple):
                for エ in ノ.elts:ナ.update(セ._extract_target_names(エ))
            return ナ
        def _extract_param_names(セ, ア_ノ: __import__('ast').arguments) -> __import__('typing').Set[str]:
            ナ = set()
            for ア in ア_ノ.posonlyargs:ナ.add(ア.arg)
            for ア in ア_ノ.args:ナ.add(ア.arg)
            if ア_ノ.vararg:ナ.add(ア_ノ.vararg.arg)
            for ア in ア_ノ.kwonlyargs:ナ.add(ア.arg)
            if ア_ノ.kwarg:ナ.add(ア_ノ.kwarg.arg)
            return ナ
        def _visit_scoped_node(セ, ノ, ロ_バ_ク):
            オ_バ = セ.バ_バ
            オ_ア = セ.ア_マ
            カ_ス_バ = オ_バ.copy()
            カ_ス_ア = オ_ア.copy()
            セ.バ_バ = カ_ス_バ
            セ.ア_マ = カ_ス_ア
            for ナ in ロ_バ_ク:セ._remove_binding(ナ)
            if isinstance(ノ, __import__('ast').Lambda):ノ.body = セ.visit(ノ.body)
            elif isinstance(ノ, (__import__('ast').FunctionDef, __import__('ast').AsyncFunctionDef)):
                セ.バ_バ = オ_バ
                セ.ア_マ = オ_ア
                ノ.decorator_list = [セ.visit(d) for d in ノ.decorator_list]
                if ノ.returns:ノ.returns = セ.visit(ノ.returns)
                セ.バ_バ = カ_ス_バ
                セ.ア_マ = カ_ス_ア
                ニ_ボ = []
                for ス in ノ.body:ニ_ボ.append(セ.visit(ス))
                ノ.body = ニ_ボ
            elif isinstance(ノ, __import__('ast').ClassDef):
                セ.バ_バ = オ_バ
                セ.ア_マ = オ_ア
                ノ.decorator_list = [セ.visit(d) for d in ノ.decorator_list]
                ノ.bases = [セ.visit(b) for b in ノ.bases]
                ノ.keywords = [セ.visit(k) for k in ノ.keywords]
                セ.バ_バ = カ_ス_バ
                セ.ア_マ = カ_ス_ア
                ニ_ボ = []
                for ス in ノ.body:ニ_ボ.append(セ.visit(ス))
                ノ.body = ニ_ボ
            elif isinstance(ノ, (__import__('ast').ListComp, __import__('ast').SetComp, __import__('ast').GeneratorExp)):
                ノ.generators = [セ.visit(g) for g in ノ.generators]
                ノ.elt = セ.visit(ノ.elt)
            elif isinstance(ノ, __import__('ast').DictComp):
                ノ.generators = [セ.visit(g) for g in ノ.generators]
                ノ.key = セ.visit(ノ.key)
                ノ.value = セ.visit(ノ.value)
            else:セ.generic_visit(ノ)
            セ.バ_バ = オ_バ
            セ.ア_マ = オ_ア
            return ノ
        def visit_Lambda(セ, ノ) -> __import__('ast').AST:
            パ_ナ = セ._extract_param_names(ノ.args)
            return セ._visit_scoped_node(ノ, パ_ナ)
        def visit_FunctionDef(セ, ノ) -> __import__('ast').AST:
            パ_ナ = セ._extract_param_names(ノ.args)
            return セ._visit_scoped_node(ノ, パ_ナ)
        def visit_AsyncFunctionDef(セ, ノ) -> __import__('ast').AST:
            パ_ナ = セ._extract_param_names(ノ.args)
            return セ._visit_scoped_node(ノ, パ_ナ)
        def visit_ListComp(セ, ノ) -> __import__('ast').AST:
            コ_バ = set()
            for コ in ノ.generators:コ_バ.update(セ._extract_target_names(コ.target))
            return セ._visit_scoped_node(ノ, コ_バ)
        def visit_SetComp(セ, ノ) -> __import__('ast').AST:
            コ_バ = set()
            for コ in ノ.generators:コ_バ.update(セ._extract_target_names(コ.target))
            return セ._visit_scoped_node(ノ, コ_バ)
        def visit_DictComp(セ, ノ) -> __import__('ast').AST:
            コ_バ = set()
            for コ in ノ.generators:コ_バ.update(セ._extract_target_names(コ.target))
            return セ._visit_scoped_node(ノ, コ_バ)
        def visit_GeneratorExp(セ, ノ) -> __import__('ast').AST:
            コ_バ = set()
            for コ in ノ.generators:コ_バ.update(セ._extract_target_names(コ.target))
            return セ._visit_scoped_node(ノ, コ_バ)
        def visit_ClassDef(セ, ノ) -> __import__('ast').AST:return セ._visit_scoped_node(ノ, set())
        def visit_Assign(セ, ノ) -> __import__('ast').AST:
            ノ.value = セ.visit(ノ.value)
            エ_ア_バ = セ.オ_セ.safe_eval_expr(ノ.value, セ.バ_バ.copy())
            if len(ノ.targets) == 1 and isinstance(ノ.targets[0], __import__('ast').Name):
                タ_ナ = ノ.targets[0].id
                if エ_ア_バ is not None:
                    セ._update_var(タ_ナ, エ_ア_バ)
                    コ_ノ = セ._create_constant_node(エ_ア_バ, ノ.value)
                    if コ_ノ is not ノ.value:ノ.value = コ_ノ
                elif isinstance(ノ.value, (__import__('ast').Name, __import__('ast').Attribute)):セ._update_alias(タ_ナ, ノ.value)
                elif isinstance(ノ.value, __import__('ast').Call) and isinstance(ノ.value.func, __import__('ast').Name) and (ノ.value.func.id == 'getattr') and (len(ノ.value.args) == 2) and isinstance(ノ.value.args[1], __import__('ast').Constant) and isinstance(ノ.value.args[1].value, str):
                    オ_ノ = ノ.value.args[0]
                    ア_ナ = ノ.value.args[1].value
                    ア_ア_ノ = セ._create_attribute_node(オ_ノ, ア_ナ, ノ.value)
                    セ._update_alias(タ_ナ, ア_ア_ノ)
                    ノ.value = ア_ア_ノ
                    セ._mark_changed()
                else:セ._remove_binding(タ_ナ)
            elif len(ノ.targets) == 1 and isinstance(ノ.targets[0], __import__('ast').Tuple):
                タ_ト = ノ.targets[0]
                バ_ト = ノ.value
                エ_ア_ト = エ_ア_バ if エ_ア_バ is not None else セ.オ_セ.safe_eval_expr(バ_ト, セ.バ_バ.copy())
                if isinstance(エ_ア_ト, tuple) and len(タ_ト.elts) == len(エ_ア_ト):
                    for イ, タ_エ in enumerate(タ_ト.elts):
                        タ_ナ = セ._extract_target_names(タ_エ)
                        for ナ in タ_ナ:セ._update_var(ナ, エ_ア_ト[イ])
                elif isinstance(バ_ト, __import__('ast').Tuple) and len(タ_ト.elts) == len(バ_ト.elts):
                    for イ, タ_エ in enumerate(タ_ト.elts):
                        タ_ナ = セ._extract_target_names(タ_エ)
                        バ_エ = バ_ト.elts[イ]
                        for ナ in タ_ナ:
                            if isinstance(バ_エ, (__import__('ast').Name, __import__('ast').Attribute)):セ._update_alias(ナ, バ_エ)
                            else:セ._remove_binding(ナ)
                else:
                    タ_ナ = セ._extract_target_names(タ_ト)
                    for ナ in タ_ナ:セ._remove_binding(ナ)
            elif len(ノ.targets) == 1:
                タ = ノ.targets[0]
                タ_ナ: __import__('typing').Optional[str] = None
                if isinstance(タ, __import__('ast').Attribute) and isinstance(タ.value, __import__('ast').Name) and (タ.value.id == 'builtins') and isinstance(タ.attr, str):
                    タ_ナ = タ.attr
                elif isinstance(タ, __import__('ast').Subscript) and isinstance(タ.value, __import__('ast').Call) and isinstance(タ.value.func, __import__('ast').Name) and (タ.value.func.id in ('vars', 'globals', 'locals')):
                    ケ = セ.オ_セ.safe_eval_expr(タ.slice, セ.バ_バ.copy())
                    if isinstance(ケ, str):タ_ナ = ケ
                if タ_ナ:
                    if エ_ア_バ is not None:
                        セ._update_var(タ_ナ, エ_ア_バ)
                        コ_ノ = セ._create_constant_node(エ_ア_バ, ノ.value)
                        if コ_ノ is not ノ.value:ノ.value = コ_ノ
                    else:セ._remove_binding(タ_ナ)
                ノ.targets = [セ.visit(t) for t in ノ.targets]
            else:ノ.targets = [セ.visit(t) for t in ノ.targets]
            return ノ
        def visit_Name(セ, ノ) -> __import__('ast').AST:
            if isinstance(ノ.ctx, __import__('ast').Load):
                if ノ.id in セ.バ_バ:
                    バ = セ.バ_バ[ノ.id]
                    コ_ノ = セ._create_constant_node(バ, ノ)
                    if コ_ノ is not ノ:
                        セ._increment_replacement_count()
                        return コ_ノ
                elif ノ.id in セ.ア_マ:
                    ア_タ = セ.ア_マ[ノ.id]
                    ビ_ア = セ.visit(ア_タ)
                    イ_セ_レ = isinstance(ビ_ア, __import__('ast').Name) and ビ_ア.id == ノ.id
                    if not イ_セ_レ:
                        __import__('ast').copy_location(ビ_ア, ノ)
                        セ._mark_changed()
                        return ビ_ア
            elif isinstance(ノ.ctx, (__import__('ast').Store, __import__('ast').Del)):セ._remove_binding(ノ.id)
            return ノ
        def visit_Attribute(セ, ノ) -> __import__('ast').AST:
            ノ.value = セ.visit(ノ.value)
            if isinstance(ノ.ctx, __import__('ast').Load):
                ベ = ノ.value
                ア_ナ = ノ.attr
                if isinstance(ベ, __import__('ast').Name) and ベ.id == 'builtins' and isinstance(ア_ナ, str) and (ア_ナ in セ.バ_バ):
                    バ = セ.バ_バ[ア_ナ]
                    コ_ノ = セ._create_constant_node(バ, ノ)
                    if コ_ノ is not ノ:
                        セ._increment_replacement_count()
                        return コ_ノ
                エ_バ = セ.オ_セ.safe_eval_expr(ノ, セ.バ_バ.copy())
                if エ_バ is not None:
                    コ_ノ = セ._create_constant_node(エ_バ, ノ)
                    if コ_ノ is not ノ:
                        セ._increment_replacement_count()
                        return コ_ノ
            return ノ
        def visit_Call(セ, ノ) -> __import__('ast').AST:
            ノ.func = セ.visit(ノ.func)
            ノ.args = [セ.visit(arg) for arg in ノ.args]
            ノ.keywords = [セ.visit(kw) for kw in ノ.keywords]
            if isinstance(ノ.func, __import__('ast').Name) and ノ.func.id == 'getattr' and (len(ノ.args) == 2) and (not ノ.keywords) and isinstance(ノ.args[1], __import__('ast').Constant) and isinstance(ノ.args[1].value, str):
                オ_ノ = ノ.args[0]
                ア_ナ = ノ.args[1].value
                ニ_ノ = セ._create_attribute_node(オ_ノ, ア_ナ, ノ)
                セ._mark_changed()
                return セ.visit(ニ_ノ)
            if isinstance(ノ.func, __import__('ast').Name) and ノ.func.id in ('eval', 'exec'):return ノ
            return ノ
        def visit_Subscript(セ, ノ) -> __import__('ast').AST:
            ノ.value = セ.visit(ノ.value)
            ノ.slice = セ.visit(ノ.slice)
            if isinstance(ノ.ctx, __import__('ast').Load):
                ベ = ノ.value
                if isinstance(ベ, __import__('ast').Call) and isinstance(ベ.func, __import__('ast').Name) and (ベ.func.id in ('vars', 'globals', 'locals')):
                    ケ = セ.オ_セ.safe_eval_expr(ノ.slice, セ.バ_バ.copy())
                    if isinstance(ケ, str):
                        if ケ in セ.バ_バ:
                            バ = セ.バ_バ[ケ]
                            コ_ノ = セ._create_constant_node(バ, ノ)
                            if コ_ノ is not ノ:
                                セ._increment_replacement_count()
                                return コ_ノ
                        elif ケ in セ.ア_マ:
                            ア_タ = セ.ア_マ[ケ]
                            ビ_ア = セ.visit(ア_タ)
                            イ_セ_レ = isinstance(ビ_ア, __import__('ast').Name) and ビ_ア.id == ケ
                            if not イ_セ_レ:
                                __import__('ast').copy_location(ビ_ア, ノ)
                                セ._mark_changed()
                                return ビ_ア
                エ_バ = セ.オ_セ.safe_eval_expr(ノ, セ.バ_バ.copy())
                if エ_バ is not None:
                    コ_ノ = セ._create_constant_node(エ_バ, ノ)
                    if コ_ノ is not ノ:
                        セ._increment_replacement_count()
                        return コ_ノ
            return ノ
        def _try_evaluate_and_replace(セ, ノ) -> __import__('ast').AST:
            if isinstance(ノ, __import__('ast').Constant):return ノ
            エ_バ = セ.オ_セ.safe_eval_expr(ノ, セ.バ_バ.copy())
            if エ_バ is not None:
                コ_ノ = セ._create_constant_node(エ_バ, ノ)
                if コ_ノ is not ノ:
                    セ._increment_replacement_count()
                    return コ_ノ
            return ノ
        def visit_UnaryOp(セ, ノ) -> __import__('ast').AST:
            ノ.operand = セ.visit(ノ.operand)
            return セ._try_evaluate_and_replace(ノ)
        def visit_BinOp(セ, ノ) -> __import__('ast').AST:
            ノ.left = セ.visit(ノ.left)
            ノ.right = セ.visit(ノ.right)
            return セ._try_evaluate_and_replace(ノ)
        def visit_Compare(セ, ノ) -> __import__('ast').AST:
            ノ.left = セ.visit(ノ.left)
            ノ.comparators = [セ.visit(c) for c in ノ.comparators]
            return セ._try_evaluate_and_replace(ノ)
        def visit_BoolOp(セ, ノ) -> __import__('ast').AST:
            ノ.values = [セ.visit(v) for v in ノ.values]
            return セ._try_evaluate_and_replace(ノ)
        def visit_IfExp(セ, ノ) -> __import__('ast').AST:
            ノ.test = セ.visit(ノ.test)
            ノ.body = セ.visit(ノ.body)
            ノ.orelse = セ.visit(ノ.orelse)
            return セ._try_evaluate_and_replace(ノ)
        def visit_Tuple(セ, ノ) -> __import__('ast').AST:
            ノ.elts = [セ.visit(e) for e in ノ.elts]
            return ノ
        def visit_List(セ, ノ) -> __import__('ast').AST:
            ノ.elts = [セ.visit(e) for e in ノ.elts]
            return ノ
        def visit_Set(セ, ノ) -> __import__('ast').AST:
            ノ.elts = [セ.visit(e) for e in ノ.elts]
            return ノ
        def visit_Dict(セ, ノ) -> __import__('ast').AST:
            ニ_ケ = []
            ニ_バ = []
            for ケ, バ in zip(ノ.keys, ノ.values):
                ビ_バ = セ.visit(バ)
                if ケ is None:
                    ニ_ケ.append(None)
                    ニ_バ.append(ビ_バ)
                else:
                    ビ_ケ = セ.visit(ケ)
                    ニ_ケ.append(ビ_ケ)
                    ニ_バ.append(ビ_バ)
            ノ.keys = ニ_ケ
            ノ.values = ニ_バ
            return ノ
    class DECODE_STRING(__import__('ast').NodeTransformer):
        def __init__(セ, デ_フ_ナ, エ_ク, フ_ト=None):
            セ.records = []
            セ.source = None
            セ.デ_ナ = set(デ_フ_ナ)
            セ.エ_コ = エ_ク
            セ.zlib = __import__('zlib')
            セ.コ_タ = (__import__('ast').Constant,)
            if __import__('sys').version_info < (3, 8):
                try:
                    セ.コ_タ += (
                        getattr(__import__('ast'), 'Str'),
                        getattr(__import__('ast'), 'Bytes'),
                        getattr(__import__('ast'), 'Num'),
                        getattr(__import__('ast'), 'NameConstant')
                    )
                except AttributeError:
                    pass
            import builtins
            セ.エ_コ.setdefault('__builtins__', builtins)
            for ナ, バ in builtins.__dict__.items():
                if ナ not in セ.エ_コ:
                    セ.エ_コ[ナ] = バ
            セ.エ_コ.setdefault('globals', lambda: セ.エ_コ)
            セ.エ_コ.setdefault('locals', lambda: セ.エ_コ)
            if セ.source:
                try:
                    モ = __import__('ast').parse(セ.source)
                    for ノ in __import__('ast').walk(モ):
                        if isinstance(ノ, __import__('ast').ImportFrom):
                            for ア in ノ.names:セ.デ_ナ.add(ア.asname or ア.name)
                except Exception:pass
            セ.パ_コ = None
            if フ_ト:
                セ.パ_コ = セ._scan_pymeo_behavior(フ_ト)
                if セ.パ_コ:
                    メ = f"Logic detected! Class: {セ.パ_コ['class_name']} | Key found."
                    if リッチ:
                         コン.print(Panel(Text(メ, style="bold green"), border_style="green", title="Pymeo Scanner", expand=False))
                    else:
                        print(f"[+] {メ}")
            セ.overall_attempt_count = 0
            セ.overall_success_count = 0
            セ.イ_フ = False
            if セ.デ_ナ and リッチ:
                コン.print(Panel(
                    Text(f"Initializing decoder process...: {list(セ.デ_ナ)}", style="italic cyan"),
                    border_style="cyan", title="Decoder Initialization", expand=False
                ))
            elif セ.デ_ナ:
                print(f"\nInitializing decoder process...: {list(セ.デ_ナ)}")
        def pymeo_decrypt(セ, ヘ_ス, ケ_バ):
            try:
                if not isinstance(ヘ_ス, str) or not isinstance(ケ_バ, bytes):
                    return None
                コ = bytes.fromhex(ヘ_ス)
                デ = セ.zlib.decompress(コ)
                デ_イ = bytearray()
                ケ_レ = len(ケ_バ)
                for イ, ビ in enumerate(デ):
                    デ_イ.append(ビ ^ ケ_バ[イ % ケ_レ])
                return デ_イ.decode('utf-8')
            except Exception:
                return None
        def _scan_pymeo_behavior(セ, ト):
            キ_ブ = set(dir(__import__('builtins')))
            for ノ in __import__('ast').walk(ト):
                if isinstance(ノ, __import__('ast').ClassDef):
                    ポ_ケ = []
                    ポ_ヘ = []
                    for サ in ノ.body:
                        if isinstance(サ, __import__('ast').Assign) and isinstance(サ.value, セ.コ_タ):
                            バ = サ.value.value
                            if isinstance(バ, bytes):
                                ポ_ケ.append(バ)
                            elif isinstance(バ, str) and len(バ) > 10:
                                ポ_ヘ.append(バ)
                    if ポ_ケ and ポ_ヘ:
                        for ケ in ポ_ケ:
                            for ヘ in ポ_ヘ:
                                レ = セ.pymeo_decrypt(ヘ, ケ)
                                if レ and レ in キ_ブ:
                                    レ_ナ = None
                                    for サ in ノ.body:
                                        if isinstance(サ, __import__('ast').FunctionDef):
                                            for チャ in __import__('ast').walk(サ):
                                                if isinstance(チャ, __import__('ast').Name) and チャ.id == 'getattr':
                                                    レ_ナ = サ.name
                                                    break
                                            if レ_ナ: break
                                    return {
                                        'class_name': ノ.name,
                                        'key': ケ,
                                        'resolve_name': レ_ナ
                                    }
            return None
        def _make_constant(セ, バ, オ_ノ):
            ニ_ノ = __import__('ast').Constant(value=バ)
            __import__('ast').copy_location(ニ_ノ, オ_ノ)
            if hasattr(オ_ノ, 'end_lineno'): ニ_ノ.end_lineno = オ_ノ.end_lineno
            if hasattr(オ_ノ, 'end_col_offset'): ニ_ノ.end_col_offset = オ_ノ.end_col_offset
            return ニ_ノ
        def _eval_node(セ, ノ, デ):
            try:
                エ = __import__('ast').Expression(body=ノ)
                コ = compile(エ, f'<deobf_{デ}>', 'eval')
                return True, eval(コ, セ.エ_コ, {})
            except Exception:
                return False, None
        def visit(セ, ノ):
            global イント
            if イント: return ノ
            return super().visit(ノ)
        def visit_ClassDef(セ, ノ):
            if セ.パ_コ and ノ.name == セ.パ_コ['class_name']:
                ニ_ボ = []
                ケ = セ.パ_コ['key']
                レ_ナ = セ.パ_コ['resolve_name']
                for サ in ノ.body:
                    if isinstance(サ, __import__('ast').Assign) and isinstance(サ.value, セ.コ_タ):
                        if isinstance(サ.value.value, str):
                            デ = セ.pymeo_decrypt(サ.value.value, ケ)
                            if デ:
                                セ.overall_success_count += 1
                                サ.value = セ._make_constant(デ, サ.value)
                    if レ_ナ and isinstance(サ, __import__('ast').FunctionDef) and サ.name == レ_ナ:
                        if len(サ.args.args) >= 2:
                            ア_ナ = サ.args.args[1].arg
                            ニ_レ = __import__('ast').Return(
                                value=__import__('ast').Call(
                                    func=__import__('ast').Name(id='getattr', ctx=__import__('ast').Load()),
                                    args=[
                                        __import__('ast').Name(id='__builtins__', ctx=__import__('ast').Load()), 
                                        __import__('ast').Name(id=ア_ナ, ctx=__import__('ast').Load())
                                    ],
                                    keywords=[]
                                )
                            )
                            サ.body = [ニ_レ]
                            if リッチ:
                                コン.print(Text(f"  > Patched resolve method: {サ.name}", style="green"))
                    ニ_ボ.append(セ.visit(サ))
                ノ.body = ニ_ボ
                return ノ
            プ_ス = セ.イ_フ
            セ.イ_フ = True 
            ノ = セ.generic_visit(ノ)
            セ.イ_フ = プ_ス
            return ノ
        def visit_FunctionDef(セ, ノ):
            プ_ス = セ.イ_フ
            セ.イ_フ = True
            ノ = セ.generic_visit(ノ)
            セ.イ_フ = プ_ス
            return ノ
        def visit_AsyncFunctionDef(セ, ノ):
            プ_ス = セ.イ_フ
            セ.イ_フ = True
            ノ = セ.generic_visit(ノ)
            セ.イ_フ = プ_ス
            return ノ
        def visit_IfExp(セ, ノ):
            ノ = セ.generic_visit(ノ)
            ス, レ = セ._eval_node(ノ.test, 'ifexp_test')
            if ス:
                return ノ.body if レ else ノ.orelse
            return ノ
        def visit_Compare(セ, ノ):
            ノ = セ.generic_visit(ノ)
            ス, レ = セ._eval_node(ノ, 'compare')
            if ス and isinstance(レ, (bool, int, float, str, bytes, type(None))):
                return セ._make_constant(レ, ノ)
            return ノ
        def visit_BinOp(セ, ノ):
            ノ = セ.generic_visit(ノ)
            ス, レ = セ._eval_node(ノ, 'binop')
            if ス and isinstance(レ, (int, float, str, bytes, bool)):
                return セ._make_constant(レ, ノ)
            return ノ
        def visit_BoolOp(セ, ノ):
            ノ = セ.generic_visit(ノ)
            ス, レ = セ._eval_node(ノ, 'boolop')
            if ス and isinstance(レ, (int, float, str, bytes, bool)):
                return セ._make_constant(レ, ノ)
            return ノ
        def visit_UnaryOp(セ, ノ):
            ノ = セ.generic_visit(ノ)
            ス, レ = セ._eval_node(ノ, 'unaryop')
            if ス and isinstance(レ, (int, float, str, bytes, bool)):
                return セ._make_constant(レ, ノ)
            return ノ
        def visit_Subscript(セ, ノ):
            ノ = セ.generic_visit(ノ)
            ス, レ = セ._eval_node(ノ, 'subscript')
            if ス and isinstance(レ, (int, float, str, bytes, bool)):
                return セ._make_constant(レ, ノ)
            return ノ
        def visit_Call(セ, ノ):
            if セ.イ_フ: 
                return セ.generic_visit(ノ)
            ノ = セ.generic_visit(ノ)
            if isinstance(ノ.func, __import__('ast').Lambda):
                ス, レ = セ._eval_node(ノ, 'lambda_call')
                if ス and isinstance(レ, (int, str, float, bool, bytes, type(None))):
                    return セ._make_constant(レ, ノ)
            オ_ア_コ = True
            for ア in ノ.args:
                if not isinstance(ア, セ.コ_タ):
                    オ_ア_コ = False
                    break
            オ_キ_コ = True
            for キ in ノ.keywords:
                 if not isinstance(キ.value, セ.コ_タ):
                    オ_キ_コ = False
                    break
            if not (オ_ア_コ and オ_キ_コ):
                return ノ
            セ.overall_attempt_count += 1
            オ_ソ = '<source not available>'
            if セ.source:
                try:
                    セグ = __import__('ast').get_source_segment(セ.source, ノ)
                    if セグ: オ_ソ = セグ.strip()
                except Exception: pass
            try:
                エ = __import__('ast').Expression(body=ノ)
                コ = compile(エ, f'<deobf_auto_call_{id(ノ)}>', 'eval')
                デ_バ = eval(コ, セ.エ_コ, {})
                if isinstance(デ_バ, (str, int, float, bool, bytes, type(None))):
                    セ.overall_success_count += 1
                    セ.records.append({
                        'lineno': getattr(ノ, 'lineno', -1),
                        'col_offset': getattr(ノ, 'col_offset', -1),
                        'original': オ_ソ,
                        'decoded': repr(デ_バ),
                    })
                    return セ._make_constant(デ_バ, ノ)
                else:
                    return ノ
            except Exception as エ:
                セ.records.append({
                    'lineno': getattr(ノ, 'lineno', -1),
                    'col_offset': getattr(ノ, 'col_offset', -1),
                    'original': オ_ソ,
                    'error': str(エ),
                })
                return ノ
__builtins__.ANTIDEBUG = False
try:
    if __name__ == '__main__':DEOBF_STRING()
except SystemExit:pass
except KeyboardInterrupt:pass
finally:pass
try:
    if リッチ:
        コン.print(Panel(
            Text(">> THANK YOU FOR USING THE TOOL <<", style="bold green"),
            border_style="green", title="Goodbye", expand=False
        ))
    else:
        __import__('sys').stdout.write("\n>> THANK YOU FOR USING THE TOOL <<\n")
        __import__('sys').stdout.flush()
except AttributeError:__builtins__.ANTIDEBUG = True
if __builtins__.ANTIDEBUG:
    raise MemoryError from None
    __import__('sys').exit(True)
__import__('sys').exit()