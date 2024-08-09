#include <stdio.h>
#include <stdlib.h>
/*


// E - Expression
//     <E> :- <T> + <E>
//          | <T> - <E>
//          | <T>
// T - Terms (multiplicative group)
//     <T> :- <V> * <T>
//         ?| <V><V>
//          | <V>
// V - Value
//     <V> :- ( <E> )
//          | <N>
// N - Number
//     <N> :- <D> <N>
//          | ε
// D - Digit
//     <D> :- 0|1|...|8|9


*/

typedef enum {
    VALUE=0,
    VARIABLE,
    ADD,
    SUB,
    MULT,
    PAREN
} node_type_t;


typedef struct node {
    node_type_t t;
    float val;
    char var;
    struct node *e1;
    struct node *e2;
} node;


// D - Digit
//     <D> :- 0|1|...|8|9
// N - Number
//     <N> :- <D> <N>
//          | ε
// V - Variable
//     <V> :- a|b|...|y|z
// S - Singleton
//     <S> :- <N>
//          | <V>
// T - Term (multiplicative group)
//     <T> :- ( <E> )
//          | <S>
// G - Group (of terms)
//     <G> :- <T> <G>
//          | <T>
// M - Multiplication
//     <M> :- <G> * <M>
//          | <G>
// E - Expression
//     <E> :- <M> + <E>
//          | <M> - <E>
//          | <M>


int cleanline(char *dirty, char *clean);
void printTree(node *n, int c);
void freeTree(node *n);
node *evalTree(node *n);
int end();
char peek();
void next();
void panic(char);
node *parseD();
node *parseN();
node *parseV();
node *parseS();
node *parseT();
node *parseG();
node *parseM();
node *parseE();
node *parse();


static char *line = NULL;
static int line_end = 0;
static int line_pos = 0;
static size_t line_len = 0; 


int
main() {
    ssize_t v = 0;
    char *buf;
    int buf_len;
    
    while (1) {
        printf("> ");
        v = getline(&buf, &buf_len, stdin );
        if( v > 0 ) {
            if( buf_len != line_len ) {
                line_len = buf_len;
                line = realloc(line, line_len);
            }
            line_end = cleanline(buf, line);
            line_pos = 0;
            
            printf("line_end: %d, v: %d\n", line_end, v);
            printf("Got Line: %s\n", line);
            
            printf("line[end]: %c\n", line[line_end]);
        }
        else {
            printf("\n");
            break;
        }

        node *e = parse();
        printf("Tree:\n");
        printTree(e, 1);
        node *t = evalTree(e);
        printf("Evaluated tree:\n");
        printTree(t, 1);
        freeTree(e);
        freeTree(t);
    }

    return 0;
}



/* Tree Building */
node *
makeVal(float v) {
    node *n;
    n = calloc(1, sizeof(node));
    n->t = VALUE;
    n->val = v;
    return n;
}
node *
makeVar(char v) {
    node *n;
    n = calloc(1, sizeof(node));
    n->t = VARIABLE;
    n->var = v;
    return n;
}
node *
makeParen(node *E) {
    node *n;
    n = calloc(1, sizeof(node));
    n->t = PAREN;
    n->e1 = E;
    return n;
}
node *
makeBinOp(node *E1, node *E2, node_type_t t) {
    node *n;
    n = calloc(1, sizeof(node));
    n->t = t;
    n->e1 = E1;
    n->e2 = E2;
    return n;
}
node *
makeAdd(node *E1, node *E2) {
    return makeBinOp(E1, E2, ADD);
}
node *
makeSub(node *E1, node *E2) {
    return makeBinOp(E1, E2, SUB);
}
node *
makeMult(node *E1, node *E2) {
    return makeBinOp(E1, E2, MULT);
}



/* Stream Functions */
int
end() {
    return ( line_pos == line_end );
}
char
peek() {
    return (end()) ? 0 : line[line_pos];
}
void
next() {
    line_pos++;
}
void panic(char c) {
    printf("Panic! (from %c)\n", c);
    exit(-1);
}



/* Grammar Parsers */
float
parseN_helper(float v) {
    char n = peek();
    if( ('0' <= n) && (n <= '9') ) {
        v *= 10;
        v += n - '0';
        next();
        return parseN_helper(v);
    }
    else {
        return v;
    }
}
node *
parseN() {
    // D - Digit
    // <D> :- 0|1|...|8|9
    // N - Number
    // <N> :- <D> <N>
    //      | ε
    float v = parseN_helper(0);
    return makeVal(v);
}
node *
parseV() {
    // V - Variable
    // <V> :- a|b|...|y|z
    char v = peek();
    if( ('a' <= v) && (v <= 'z') ) {
        next();
        return makeVar(v);
    }
    panic('V');
}
node *
parseS() {
    // S - Singleton
    // <S> :- <N>
    //      | <V>
    char c = peek();
    if( ('0' <= c) && (c <= '9') ) {
        return parseN();
    } else if ( ('a' <= c) && (c <= 'z') ) {
        printf("In parseS case\n");
        return parseV();
    }
    panic('S');
}
node *
parseT() {
    // T - Term (multiplicative group)
    // <T> :- ( <E> )
    //      | <S>
    if( peek() == '(' ) {
        next();
        node *E = parseE();
        if( peek() != ')' ) {
            panic('T');
        }
        next();
        return E;
        // return makeParen(E);
    }
    return parseS();
}
int
is_S() {
    // S - Singleton
    // <S> :- <N>
    //      | <V>
    char c = peek();
    if( ('0' <= c) && (c <= '9') ) {
        return 1;
    }
    if ( ('a' <= c) && (c <= 'z') ) {
        return 1;
    }
    return 0;
}
int
is_T() {
    // T - Term (multiplicative group)
    // <T> :- ( <E> )
    //      | <S>
    return !!( is_S() || (peek() == '(') );
}
node *
parseG() {
    // G - Group (of terms)
    // <G> :- <T> <G>
    //      | <T>
    node *T = parseT();        
    if( is_T() ) {
        return makeMult(T, parseG());
    }
    return T;
}
node *
parseM() {
    // M - Multiplication
    // <M> :- <G> * <M>
    //      | <G>
    node *G = parseG();
    if( peek() == '*' ) {
        next();
        return makeMult(G, parseM());
    }
    return G;
}
node *
parseE() {
    // E - Expression
    // <E> :- <M> + <E>
    //      | <M> - <E>
    //      | <M>
    node *M = parseM();
    char op = peek();
    switch (op) {
        case '+':
            next();
            return makeAdd(M, parseE());
        case '-':
            next();
            return makeSub(M, parseE());
        default:
            return M;
    }
}
node *
parse() {
    node *n = parseE();
    if( !end() ) {
        printf("DID NOT REACH END\n  line_pos: %d | peek(): %c\n", line_pos, peek());
    }
    return n;
}





/* General Help */
node *
addEval(node *n) {
    node *l = evalTree(n->e1);
    node *r = evalTree(n->e2);

    if( (l->t == VALUE) && (r->t == VALUE) ) {
        float val = l->val + r->val;
        free(l);
        free(r);
        return makeVal(val);
    }
    if( (l->t == VALUE) && (l->val == 0) ) {
        free(l);
        return r;
    }
    if( (r->t == VALUE) && (r->val == 0) ) {
        free(r);
        return l;
    }
    return makeAdd(l, r);
}

node *
subEval(node *n) {
    node *l = evalTree(n->e1);
    node *r = evalTree(n->e2);

    if( (l->t == VALUE) && (r->t == VALUE) ) {
        float val = l->val - r->val;
        free(l);
        free(r);
        return makeVal(val);
    }
    if( (r->t == VALUE) && (r->val == 0) ) {
        free(r);
        return l;
    }
    return makeSub(l, r);
}
node *
distribute(node *l, node *r) {
    node *v;
    // Distrubutes the VALUE node l on r
    switch (r->t) {
        case MULT:
            v = makeMult(evalTree(makeMult(makeVal(l->val), r->e1)),
                         evalTree(makeMult(makeVal(l->val), r->e2)));
            freeTree(l);
            // leave r->e1 and r->e2 
            free(r);
            return v;
        case ADD:
            v = makeAdd(evalTree(makeMult(makeVal(l->val), r->e1)),
                        evalTree(makeMult(makeVal(l->val), r->e2)));
            freeTree(l);
            // leave r->e1 and r->e2 
            free(r);
            return v;
        case SUB:
            v = makeSub(evalTree(makeMult(makeVal(l->val), r->e1)),
                        evalTree(makeMult(makeVal(l->val), r->e2)));
            freeTree(l);
            // leave r->e1 and r->e2 
            free(r);
            return v;
    }
}

node *
multEval(node *n) {
    node *l = evalTree(n->e1);
    node *r = evalTree(n->e2);

    if( (l->t == VALUE) && (r->t == VALUE) ) {
        float val = l->val * r->val;
        free(l);
        free(r);
        return makeVal(val);
    }
    if( l->t == VALUE ) {
        if( l->val == 0 ) {
            freeTree(l);
            freeTree(r);
            return makeVal(0);
        }
        if( r->t == VARIABLE ) {
            return makeMult(l, r);
        }
        return distribute(l, r);
    }
    if( r->t == VALUE ) {
        if( r->val == 0 ) {
            freeTree(l);
            freeTree(r);
            return makeVal(0);
        }
        if( l->t == VARIABLE ) {
            return makeMult(l, r);
        }
        return distribute(r, l);
    }
    return makeMult(l, r);
}


node *
evalTree(node *n) {
    switch (n->t) {
        case PAREN:
            return evalTree(n->e1);
        case VALUE:
            return makeVal(n->val);
        case VARIABLE:
            return makeVar(n->var);
        case ADD:
            return addEval(n);
        case SUB:
            return subEval(n);
        case MULT:
            return multEval(n);
        default:
            printf("evalTree hit default case\n");
    }
}

void
freeTree(node *n) {
    if( n->e1 ) freeTree(n->e1);
    if( n->e2 ) freeTree(n->e2);
    free(n);
}


void
printSpace(int n) {
    for( int i = 0; i < n; i++ )
        printf(" ");
}

void
printTree(node *n, int c) {
    switch (n->t) {
        case PAREN:
            printSpace(c);
            printf("(\n");
            printTree(n->e1, c+1);
            printSpace(c);
            printf(")\n");
            break;
        case VALUE:
            printSpace(c);
            printf("%f\n", n->val);
            break;
        case VARIABLE:
            printSpace(c);
            printf("%c\n", n->var);
            break;
        case ADD:
            printTree(n->e1, c+1);
            printSpace(c);
            printf("+\n");
            printTree(n->e2, c+1);
            break;
        case SUB:
            printTree(n->e1, c+1);
            printSpace(c);
            printf("-\n");
            printTree(n->e2, c+1);
            break;
        case MULT:
            printTree(n->e1, c+1);
            printSpace(c);
            printf("*\n");
            printTree(n->e2, c+1);
            break;
    }
}

int
cleanline(char *dirty, char *clean) {
    char *q = clean;
    for( char *p = dirty; *p != 0; p++ ) {
        if( *p > 32 ) {
            *q = *p;
            q++;
        }
    }
    *q = 0;
    return (int)(q - clean);
}
