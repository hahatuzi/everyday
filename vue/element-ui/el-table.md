```js
  ::v-deep.el-table {
    background-color: transparent;

    &:before {
      height: 0;
    }

    tr {
      background-color: transparent;
    }

    .el-table__cell.gutter {
      display: none;
    }

    .cell {
      line-height: inherit;
    }

    .el-table__row{
      &.current-row, &:hover {
        color: #fff;
        cursor: pointer;
        background-color: rgb(82,131,189);
      }

      &.el-table__row--striped {
        td {
          background-color: rgba(32, 110, 212, 0.34) !important;
        }
      }
    }
  }
```