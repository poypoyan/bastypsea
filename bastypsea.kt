/*
Basic Type Search (bastypsea) for Apex language
By poypoyan

Implemented in Kotlin/JVM 1.9.10 and Java 17.0.8
Compile command: kotlinc bastypsea.kt -include-runtime -d bastypsea.jar
Run command: java -jar bastypsea.jar

Distributed under the MIT software license. See the accompanying
file LICENSE or https://opensource.org/license/mit/.
*/
package org.bastypsea

import kotlin.io.path.Path
import kotlin.io.path.listDirectoryEntries
import java.nio.file.Path
import java.nio.file.Files
import java.nio.file.Files.newBufferedReader

data class VarEntry(val lineN: Int, val name: String)
data class OutputEntry(val initLineN: Int, val lineN: Int, val pline: String)

class ApexCodeState(val PATH: Path, val OBJ: String, val ACT: String, val IS_IGNORE_TEST: Boolean) {
    val DELIMS = arrayOf<String>("//", "/*", "*/", ";", "{", "}")
    val vars = mutableListOf<VarEntry>()
    val types = mutableListOf<String>(OBJ)
    var IS_CHECK_VAR_ONLY = false
    var line = 1
    var isComment = false
    var isTestClass = false

    private val _RGX_CLASS = Regex("^[a-z\\s]+\\sclass\\s+([a-z0-9_]+)", RegexOption.IGNORE_CASE)
    private val _RGX_DMLS = arrayOf<Regex?>(null, null)
    private var _lastDelim = -1
    private var _curlyBracketCtr = 0
    private var _candInnerClass = ""
    private var _lineInnerClass = 0
    private var _isInOuterClass = false
    private var _isInInnerClass = false

    init {
        if (ACT == "")
            IS_CHECK_VAR_ONLY = true
        else {
            _RGX_DMLS[0] = Regex("[^.]${ACT}\\s+([a-z0-9_]+)", RegexOption.IGNORE_CASE)   // DML
            _RGX_DMLS[1] = Regex("Database.${ACT}[a-z]*\\s*\\(\\s*([a-z0-9_]+)", RegexOption.IGNORE_CASE)   // Database method
        }
    }

    fun procLineStop(line: String, founds: MutableList<OutputEntry>): Boolean {
        val STOP = true
        var partStart = 0
        var iPlus: Int

        for (i in 0..<line.length) {
            for (j in this.DELIMS.indices) {
                iPlus = i + this.DELIMS[j].length
                if (line.substring(i..<Math.min(line.length, iPlus)) == this.DELIMS[j] && (j < 3 || (3 <= j && !this.isComment))) {
                    this.updFromPline(line.substring(partStart..<Math.min(line.length, iPlus)), j, founds)
                    if (this.IS_IGNORE_TEST && this.isTestClass) return STOP
                    partStart = iPlus
                }
            }
        }
        this.updFromPline(line.substring(partStart..<line.length), -1, founds)
        if (this.IS_IGNORE_TEST && this.isTestClass) return STOP
        return !STOP
    }

    fun updFromPline(pline: String, delim: Int, founds: MutableList<OutputEntry>) {
        if (this.isComment) {
            this._updFromDelim(delim)
            return
        }

        // search for var init
        if(!this._isInInnerClass) {
            val resVarInit = this._checkVarInit(pline)
            if (resVarInit?.groupValues != null) {
                // insert to this.vars as first element so that latest
                // added is checked first on this._resFromAction
                this.vars.add(0, VarEntry(this.line, resVarInit.groupValues[1]))
                this._updFromDelim(delim)
                return
            }
        }

        // search for outer class init
        val resOutClass = this._RGX_CLASS.find(pline)
        if (!this._isInOuterClass) {
            // check if test class
            if (pline.contains("@istest", ignoreCase = true)) this.isTestClass = true
            if (resOutClass?.groupValues != null) this._isInOuterClass = true
            this._updFromDelim(delim)
            return
        }

        // search for var in inner class
        if (this._isInInnerClass) {
            if (!this.IS_CHECK_VAR_ONLY && this.types[0] != this._candInnerClass) {
                val resInClass = this._checkVarInit(pline)
                if (resInClass?.groupValues != null) {
                    this.types.add(0, this._candInnerClass)
                    // backtrack file from start to where inner class is initialized
                    // so that vars init BEFORE inner class init are detected
                    val backCodeState = ApexCodeState(this.PATH, this._candInnerClass, "", true)
                    _bastypseaFull(this.PATH, backCodeState, this._lineInnerClass)
                    this.vars += backCodeState.vars
                }
            }
            when (delim) {
                4 -> this._curlyBracketCtr += 1
                5 -> this._curlyBracketCtr -= 1
            }
            if (this._curlyBracketCtr == 0) this._isInInnerClass = false
            this._updFromDelim(delim)
            return
        }

        // else, search for inner class init
        if (resOutClass?.groupValues != null) {
            this._isInInnerClass = true
            this._curlyBracketCtr = 1
            this._candInnerClass = resOutClass.groupValues[1]
            this._lineInnerClass = this.line
            this._updFromDelim(delim)
            return
        }

        if (this.IS_CHECK_VAR_ONLY) {
            this._updFromDelim(delim)
            return
        }

        // search for action
        for (i in this._RGX_DMLS) {
            val resDML = i?.find(pline)
            if (resDML?.groupValues != null) {
                this._resFromAction(resDML, pline, founds)
                this._updFromDelim(delim)
                return
            }
        }

        this._updFromDelim(delim)
    }

    private fun _checkVarInit(pline: String): MatchResult? {
        for (i in this.types) {
            val rgxVarInit = Regex("[a-z0-9_,<>\\s]*${i}[a-z0-9_,<>\\s]*\\s+([a-z0-9_]+)", RegexOption.IGNORE_CASE)
            val res = rgxVarInit.find(pline)
            if (res?.groupValues != null) return res
        }
        return null
    }

    private fun _resFromAction(res: MatchResult, pline: String, founds: MutableList<OutputEntry>): Boolean {
        for (i in this.vars.indices) {
            if (res.groupValues[1] == this.vars[i].name) {
                founds.add(OutputEntry(this.vars[i].lineN, this.line, pline.trimIndent()))
                this.vars.removeAt(i)
                return true
            }
        }
        return false
    }

    private fun _updFromDelim(delim: Int) {
        if (delim in 0..<3) this._lastDelim = delim
        when (delim) {
            0, 1 -> this.isComment = true
            2 -> this.isComment = false
        }
    }

    fun updFromNewLine() {
        this.line += 1
        if (this._lastDelim == 0) this.isComment = false
    }
}

private fun _bastypseaFull(path: Path, codeState: ApexCodeState, lastLine: Int): MutableList<OutputEntry> {
    val founds = mutableListOf<OutputEntry>()

    val br = newBufferedReader(path)
    while (true) {
        val line = br.readLine()
        // bastypsea proper
        // https://www.youtube.com/watch?v=JbpRzghAlBM
        if (line == null || codeState.procLineStop(line, founds) || codeState.line == lastLine) break
        codeState.updFromNewLine()
    }
    br.close()

    return founds
}

fun btsRun(path: Path, inputObj: String, inputAct: String, ignoreTest: Boolean = true): MutableList<OutputEntry> {
    val codeState = ApexCodeState(path, inputObj, inputAct, ignoreTest)
    return _bastypseaFull(path, codeState, -1)
}

fun main(args: Array<String>) {
    val help =
    """
    Usage: bastypsea.jar <Object> <Action> <Path> ["addTest"]

    Note that Path can be a directory like "./classes/" or
    a file like "./classes/MyApexClass.cls". For the case
    of directory, only .cls files are scanned.
    """.trimIndent()
    val classes: List<Path>

    if (!(args.size in 3..4) || (args.size == 4 && args[3] != "addTest")) {
        println(help)
        return
    }

    val path = Path(args[2])
    if (!Files.exists(path)) {
        System.err.println("Error: path does not exist.")
        return
    }
    if (Files.isRegularFile(path)) classes = listOf<Path>(path)
    else if(Files.isDirectory(path)) classes = path.listDirectoryEntries("*.cls")
    else {
        System.err.println("Error: path exists, but is unsupported.")
        return
    }

    classes.forEach {cls ->
        var isIgnoreTest = true
        if (args.size == 4) isIgnoreTest = false
        val outputs = btsRun(cls, args[0], args[1], isIgnoreTest)

        if (outputs.size > 0) {
            println(cls.toString() + ":")
            outputs.forEach {
                println(
                """
                initN: ${it.initLineN}
                lineN: ${it.lineN}
                pline: ${it.pline}
                ------
                """.trimIndent()
                )
            }
        }
    }
}
